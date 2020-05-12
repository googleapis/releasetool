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

import click

import releasetool.circleci
import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common
from releasetool.commands.common import TagContext

RELEASE_NOTES_HEADER_PATTERNS = [
    r"This pull request was generated using releasetool\.\s+(.*)",
    r":robot: .*\n---(.*)\n---",
]


def determine_release_pr(ctx: TagContext) -> None:
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


def _parse_release_tag(head_ref: str) -> str:
    match = re.match(r"release.*-(v\d+\.\d+\.\d+)", head_ref)
    return match.group(1) if match else None


def determine_release_tag(ctx: TagContext) -> None:
    click.secho("> Determining what the release tag should be.", fg="cyan")
    head_ref = ctx.release_pr["head"]["ref"]
    ctx.release_tag = _parse_release_tag(head_ref)

    if ctx.release_tag is None:
        click.secho(
            "I couldn't determine what the release tag should be from the PR's"
            f"head ref {head_ref}.",
            fg="red",
        )
        ctx.release_tag = click.prompt(
            "What should the release tag be (for example, storage-1.2.3)?"
        )

    click.secho(f"Release tag is {ctx.release_tag}.")


def determine_package_name_and_version(ctx: TagContext) -> None:
    click.secho("> Determining the release version.", fg="cyan")
    match = re.match(r"v(\d+\.\d+\.\d+)", ctx.release_tag)
    ctx.release_version = match.group(1)
    click.secho(f"Package version: {ctx.release_version}.")


def _parse_release_notes(pr_body) -> str:
    for pattern in RELEASE_NOTES_HEADER_PATTERNS:
        match = re.search(pattern, pr_body, re.DOTALL | re.MULTILINE)
        if match is not None:
            return match.group(1).strip()

    return ""


def get_release_notes(ctx: TagContext) -> None:
    click.secho("> Grabbing the release notes.", fg="cyan")
    ctx.release_notes = _parse_release_notes(ctx.release_pr["body"])
    click.secho(f"Release notes:\n{ctx.release_notes}")


def create_release(ctx: TagContext) -> None:
    click.secho("> Creating the release.")

    ctx.github_release = ctx.github.create_release(
        repository=ctx.upstream_repo,
        tag_name=ctx.release_tag,
        target_commitish=ctx.release_pr["merge_commit_sha"],
        name=ctx.release_tag,
        body=ctx.release_notes,
    )

    release_location_string = f"Release is at {ctx.github_release['html_url']}"
    click.secho(release_location_string)

    ctx.github.create_pull_request_comment(
        ctx.upstream_repo, ctx.release_pr["number"], release_location_string
    )

    repo_short_name = ctx.upstream_repo.split("/")[-1]
    ctx.kokoro_job_name = (
        f"cloud-devrel/client-libraries/java/{repo_short_name}/release/stage"
    )
    ctx.github.update_pull_labels(
        ctx.release_pr, add=["autorelease: tagged"], remove=["autorelease: pending"]
    )
    releasetool.commands.common.publish_via_kokoro(ctx)


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
    determine_package_name_and_version(ctx)

    # If the release already exists, don't do anything
    if releasetool.commands.common.release_exists(ctx):
        click.secho(f"{ctx.release_tag} already exists.", fg="magenta")
        return ctx

    get_release_notes(ctx)
    create_release(ctx)

    if ctx.interactive:
        click.secho("\\o/ All done!", fg="magenta")

    return ctx
