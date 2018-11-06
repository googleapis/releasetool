# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import Optional, Sequence, Tuple
from urllib import parse

import attr
import click
import pyperclip
from dateutil import tz

import releasetool.filehelpers
import releasetool.git
import releasetool.github
import releasetool.secrets


@attr.s(auto_attribs=True, slots=True)
class BaseContext:
    interactive: bool = True


@attr.s(auto_attribs=True, slots=True)
class GitHubContext(BaseContext):
    github: Optional[releasetool.github.GitHub] = None
    origin_user: Optional[str] = None
    origin_repo: Optional[str] = None
    upstream_name: Optional[str] = None
    upstream_repo: Optional[str] = None
    package_name: Optional[str] = None
    changes: Sequence[str] = ()
    release_notes: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class TagContext(GitHubContext):
    release_pr: Optional[dict] = None
    release_tag: Optional[str] = None
    release_version: Optional[str] = None
    github_release: Optional[dict] = None
    kokoro_job_name: Optional[str] = None
    fusion_url: Optional[str] = None


def _determine_origin(ctx: GitHubContext) -> None:
    remotes = releasetool.git.get_github_remotes()
    origin = remotes["origin"]
    ctx.origin_user = origin.split("/")[0]
    ctx.origin_repo = origin


def _determine_upstream(ctx: GitHubContext, owners: Tuple[str, ...]) -> None:
    remotes = releasetool.git.get_github_remotes()
    repos = {
        name: repo for name, repo in remotes.items() if repo.lower().startswith(owners)
    }

    if not repos:
        raise ValueError("Unable to determine the upstream GitHub repo. :(")

    if len(repos) > 1:
        options = "\n".join(f"  * {name}: {repo}" for name, repo in repos.items())
        choice = click.prompt(
            click.style(
                f"More than one possible upstream remote was found."
                f"\n\n{options}\n\n"
                f"Please enter the *name* of one you want to use",
                fg="yellow",
            )
        )
        try:
            upstream = choice, repos[choice]
        except KeyError:
            click.secho(f"No remote named {choice}!", fg="red")
            raise click.Abort()
    else:
        upstream = repos.popitem()

    ctx.upstream_name, ctx.upstream_repo = upstream


def setup_github_context(
    ctx: GitHubContext,
    owners: Tuple[str, ...] = ("googlecloudplatform", "googleapis", "google"),
) -> None:
    click.secho("> Determining GitHub context.", fg="cyan")
    github_token = releasetool.secrets.ensure_password(
        "github",
        "Please provide your GitHub API token with write:repo_hook and "
        "public_repo (https://github.com/settings/tokens)",
    )
    ctx.github = releasetool.github.GitHub(github_token)

    _determine_origin(ctx)
    _determine_upstream(ctx, owners)

    click.secho(f"Origin: {ctx.origin_repo}, Upstream: {ctx.upstream_repo}")

    # Compare upstream/master with master
    click.secho(f"> Comparing {ctx.upstream_name}/master to master.", fg="cyan")

    if releasetool.git.get_latest_commit(
        f"{ctx.upstream_name}/master"
    ) == releasetool.git.get_latest_commit("master"):
        click.echo(f"master is up to date with {ctx.upstream_name}/master")
    else:
        click.secho(
            f"WARNING: master is not up to date with {ctx.upstream_name}/master",
            fg="red",
        )
        if click.confirm("> Would you like to continue?") is False:
            exit()


def edit_release_notes(ctx: GitHubContext) -> None:
    click.secho(f"> Opening your editor to finalize release notes.", fg="cyan")
    release_notes = (
        datetime.datetime.now(datetime.timezone.utc)
        .astimezone(tz.gettz("US/Pacific"))
        .strftime("%m-%d-%Y %H:%M %Z\n\n")
    )
    release_notes += "\n".join(f"- {change}" for change in ctx.changes)
    release_notes += "\n\n### ".join(
        [
            "",
            "Implementation Changes",
            "New Features",
            "Dependencies",
            "Documentation",
            "Internal / Testing Changes",
        ]
    )
    ctx.release_notes = releasetool.filehelpers.open_editor_with_tempfile(
        release_notes, "release-notes.md"
    ).strip()

def exists_release(ctx: TagContext) -> bool:
    release = ctx.github.get_release(ctx.upstream_repo, ctx.release_tag)
    tag_sha = ctx.github.get_tag_sha(ctx.upstream_repo, ctx.release_tag)

    if release is not None and tag_sha == ctx.release_pr["merge_commit_sha"]:
        return True
    else:
        return False

def publish_via_kokoro(ctx: TagContext) -> None:
    kokoro_url = "https://fusion.corp.google.com/projectanalysis/current/KOKORO/"

    ctx.kokoro_job_name = f"cloud-devrel/client-libraries/{ctx.package_name}/release"
    ctx.fusion_url = parse.urljoin(
        kokoro_url, parse.quote_plus(f"prod:{ctx.kokoro_job_name}")
    )

    if ctx.interactive:
        pyperclip.copy(ctx.release_tag)

        click.secho(
            f"> Trigger the Kokoro build with the commitish below to publish to PyPI. The commitish has been copied to the clipboard.",
            fg="cyan",
        )

    click.secho(f"Kokoro build URL:\t\t{click.style(ctx.fusion_url, underline=True)}")
    click.secho(f"Commitish:\t{click.style(ctx.release_tag, bold=True)}")

    if ctx.interactive:
        if click.confirm("Would you like to go the Kokoro build page?", default=True):
            click.launch(ctx.fusion_url)
