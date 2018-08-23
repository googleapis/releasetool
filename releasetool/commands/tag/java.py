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
from typing import Optional

import attr
import click

import releasetool.circleci
import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common


@attr.s(auto_attribs=True, slots=True)
class Context(releasetool.commands.common.GitHubContext):
    package_name: Optional[str] = None
    release_pr: Optional[dict] = None
    release_tag: Optional[str] = None
    release_version: Optional[str] = None
    release_notes: Optional[str] = None
    github_release: Optional[dict] = None


def determine_release_pr(ctx: Context) -> None:
    click.secho(
        "> Let's figure out which pull request corresponds to your release.", fg="cyan"
    )

    pulls = ctx.github.list_pull_requests(ctx.upstream_repo, state="closed")
    pulls = [pull for pull in pulls if "release" in pull["title"].lower()][:30]

    click.secho("> Please pick one of the following PRs:\n")
    for n, pull in enumerate(pulls, 1):
        print(f"\t{n}: {pull['title']} ({pull['number']})")

    pull_idx = click.prompt("\nWhich one do you want to tag and release?", type=int)

    ctx.release_pr = pulls[pull_idx - 1]


def determine_release_tag(ctx: Context) -> None:
    click.secho("> Determining what the release tag should be.", fg="cyan")
    head_ref = ctx.release_pr["head"]["ref"]
    match = re.match("release-.+-(v\d+\.\d+\.\d+)", head_ref)

    if match is not None:
        ctx.release_tag = match.group(1)
    else:
        print(
            "I couldn't determine what the release tag should be from the PR's"
            f"head ref {head_ref}."
        )
        ctx.release_tag = click.prompt(
            "What should the release tag be (for example, storage-1.2.3)?"
        )

    click.secho(f"Release tag is {ctx.release_tag}.")


def determine_package_name_and_version(ctx: Context) -> None:
    click.secho("> Determining the release version.", fg="cyan")
    match = re.match("v(\d+\.\d+\.\d+)", ctx.release_tag)
    ctx.release_version = match.group(1)
    click.secho(
        f"Package version: {ctx.release_version}."
    )


def get_release_notes(ctx: Context) -> None:
    click.secho("> Grabbing the release notes.", fg="cyan")

    match = re.search(
        r"This pull request was generated using releasetool\.\n\n(.*)",
        ctx.release_pr["body"],
        re.DOTALL | re.MULTILINE,
    )
    if match is not None:
        ctx.release_notes = match.group(1).strip()
    else:
        ctx.release_notes = ""

    click.secho(f"Release notes:\n{ctx.release_notes}")


def create_release(ctx: Context) -> None:
    click.secho("> Creating the release.")

    ctx.github_release = ctx.github.create_release(
        repository=ctx.upstream_repo,
        tag_name=ctx.release_version,
        target_committish=ctx.release_pr["merge_commit_sha"],
        name=f"{ctx.release_version}",
        body=ctx.release_notes,
    )

    release_location_string = f"Release is at {ctx.github_release['html_url']}"
    click.secho(release_location_string)

    ctx.github.create_pull_request_comment(
        ctx.upstream_repo, ctx.release_pr["number"], release_location_string
    )


def tag() -> None:
    ctx = Context()

    click.secho(f"o/ Hey, {getpass.getuser()}, let's tag a release!", fg="magenta")

    releasetool.commands.common.setup_github_context(ctx)

    determine_release_pr(ctx)
    determine_release_tag(ctx)
    determine_package_name_and_version(ctx)
    get_release_notes(ctx)

    create_release(ctx)

    click.secho(f"\o/ All done!", fg="magenta")
