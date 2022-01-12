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

import getpass
import re
from typing import List, Union

import click

import releasetool.circleci
import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common
from releasetool.commands.common import TagContext


def determine_release_pr(ctx: TagContext) -> None:
    click.secho(
        "> Let's figure out which pull request corresponds to your release.", fg="cyan"
    )

    pulls = ctx.github.list_pull_requests(ctx.upstream_repo, state="closed")
    pulls = [pull for pull in pulls if "release" in pull["title"].lower()][:30]

    click.secho("> Please pick one of the following PRs:\n")
    for n, pull in enumerate(pulls, 1):
        print(f"\t{n}: {pull['title']} ({pull['number']})")

    pull_idx = click.prompt(
        "\nWhich one do you want to tag and release?", type=click.INT
    )

    ctx.release_pr = pulls[pull_idx - 1]


def determine_release_tag(ctx: TagContext) -> None:
    click.secho("> Determining what the release tag should be.", fg="cyan")
    head_ref = ctx.release_pr["head"]["ref"]

    # try release-please v13 pull requests
    title = ctx.release_pr["title"]
    match = re.match("chore\\(.*\\): release (\\d+\\.\\d+\\.\\d+.*)", title)
    if match is not None:
        ctx.release_tag = f"v{match.group(1)}"
        return

    match = re.match("release-(.+)", head_ref)

    if match is not None:
        ctx.release_tag = match.group(1)
    else:
        print(
            "I couldn't determine what the release tag should be from the PR's"
            f"head ref {head_ref}."
        )
        ctx.release_tag = click.prompt(
            "What should the release tag be (for example, v1.2.3)?"
        )

    click.secho(f"Release tag is {ctx.release_tag}.")


def determine_package_version(ctx: TagContext) -> None:
    click.secho("> Determining the package version.", fg="cyan")
    # strip the leading 'v' from the tag
    ctx.release_version = re.sub(r"^v", "", ctx.release_tag)
    click.secho(f"Package version: {ctx.release_version}.")


def get_release_notes(ctx: TagContext) -> None:
    click.secho("> Grabbing the release notes.")

    changelog_path = "CHANGELOG.md"
    changelog = ctx.github.get_contents(
        ctx.upstream_repo, changelog_path, ref=ctx.release_pr["merge_commit_sha"]
    ).decode("utf-8")

    _get_latest_release_notes(ctx, changelog)


def _get_latest_release_notes(ctx: TagContext, changelog: str):
    match = re.search(
        rf"## v?\[?{ctx.release_version}[^\n]*\n(?P<notes>.+?)(\n##\s|\n### \[?[0-9]+\.|\Z)",
        changelog,
        re.DOTALL | re.MULTILINE,
    )
    if match is not None:
        ctx.release_notes = match.group("notes").strip()
    else:
        ctx.release_notes = ""


def create_release(ctx: TagContext) -> None:
    click.secho("> Creating the release.")

    release_name = f"v{ctx.release_version}"
    ctx.github_release = ctx.github.create_release(
        repository=ctx.upstream_repo,
        tag_name=ctx.release_tag,
        target_commitish=ctx.release_pr["merge_commit_sha"],
        name=release_name,
        body=ctx.release_notes,
    )

    release_location_string = f"Release is at {ctx.github_release['html_url']}"
    click.secho(release_location_string)

    ctx.github.create_pull_request_comment(
        ctx.upstream_repo, ctx.release_pr["number"], release_location_string
    )

    ctx.github.update_pull_labels(
        ctx.release_pr, add=["autorelease: tagged"], remove=["autorelease: pending"]
    )


"""A list of repositories that have been migrated to use the new KOKORO VM
   pool dedicated to releasing client libraries.
"""
release_pool_repos: List[str] = ["googleapis/python-apigee-connect"]


def kokoro_job_name(upstream_repo: str, package_name: str) -> Union[str, None]:
    """Return the Kokoro job name.

    Args:
        upstream_repo (str): The GitHub repo in the form of `<owner>/<repo>`
        package_name (str): The name of package to release

    Returns:
        The name of the Kokoro job to trigger or None if there is no job to trigger
    """
    if upstream_repo in release_pool_repos:
        return f"cloud-devrel/client-libraries/release/python/{upstream_repo}/release"
    else:
        return f"cloud-devrel/client-libraries/python/{upstream_repo}/release/release"


def package_name(pull: dict) -> Union[str, None]:
    return None


def tag(ctx: TagContext = None) -> TagContext:
    if not ctx:
        ctx = TagContext()

    if ctx.interactive:
        click.secho(f"o/ Hey, {getpass.getuser()}, let's tag a release!", fg="magenta")

    if ctx.github is None:
        releasetool.commands.common.setup_github_context(ctx)

    if ctx.release_pr is None:
        determine_release_pr(ctx)

    determine_release_tag(ctx)
    determine_package_version(ctx)

    # If the release already exists, don't do anything
    if releasetool.commands.common.release_exists(ctx):
        click.secho(f"{ctx.release_tag} already exists.", fg="magenta")
        return ctx

    get_release_notes(ctx)

    create_release(ctx)

    ctx.kokoro_job_name = kokoro_job_name(ctx.upstream_repo, ctx.package_name)
    releasetool.commands.common.publish_via_kokoro(ctx)

    if ctx.interactive:
        click.secho("\\o/ All done!", fg="magenta")

    return ctx
