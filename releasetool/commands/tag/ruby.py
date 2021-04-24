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
from typing import Union

import click
from requests import HTTPError

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

    pull_idx = click.prompt("\nWhich one do you want to tag and release?", type=int)

    ctx.release_pr = pulls[pull_idx - 1]


def determine_release_tag(ctx: TagContext) -> None:
    click.secho("> Determining the release tag.", fg="cyan")
    head_ref = ctx.release_pr["head"]["ref"]
    click.secho(f"PR head ref is {head_ref}")
    match = re.match(r"release-(.+)-v(\d+\.\d+\.\d+)", head_ref)

    if match is not None:
        ctx.package_name = match.group(1)
        ctx.release_version = match.group(2)
        ctx.release_tag = f"{ctx.package_name}/v{ctx.release_version}"
    else:
        click.secho(
            "I couldn't determine what the release tag should be from the PR's"
            f"head ref {head_ref}.",
            fg="red",
        )
        ctx.release_tag = click.prompt(
            "What should the release tag be (for example, google-cloud-storage/v1.2.3)?"
        )

    click.secho(f"Package name is {ctx.package_name}")
    click.secho(f"Package version is {ctx.release_version}")
    click.secho(f"Release tag is {ctx.release_tag}")


def determine_package_name_and_version(ctx: TagContext) -> None:
    click.secho(
        "> Determining the package name and version from your release tag.", fg="cyan"
    )
    match = re.match(r"^([a-z0-9-_]+)\/v(\d+.\d+.\d+)$", ctx.release_tag)
    ctx.package_name = match.group(1)
    ctx.release_version = match.group(2)


def get_release_notes(ctx: TagContext) -> None:
    click.secho("> Grabbing the release notes.", fg="cyan")
    if (
        "google-cloud-ruby" in ctx.upstream_repo
        or "google-api-ruby-client" in ctx.upstream_repo
    ):
        changelog_file = f"{ctx.package_name}/CHANGELOG.md"
    else:
        changelog_file = "CHANGELOG.md"
    changelog = ctx.github.get_contents(
        ctx.upstream_repo, changelog_file, ref=ctx.release_pr["merge_commit_sha"]
    ).decode("utf-8")

    match = re.search(
        rf"^### {ctx.release_version} \/ \d\d\d\d-\d\d-\d\d\n(?P<notes>.+?)(\n###\s|\Z)",
        changelog,
        re.DOTALL | re.MULTILINE,
    )
    if match is not None:
        ctx.release_notes = match.group("notes").strip()
    else:
        ctx.release_notes = ""

    click.secho(f"Here's the release notes:\n\n{ctx.release_notes}\n")


def create_release(ctx: TagContext) -> None:
    click.secho("> Creating the release.")

    ctx.github_release = ctx.github.create_release(
        repository=ctx.upstream_repo,
        tag_name=ctx.release_tag,
        target_commitish=ctx.release_pr["merge_commit_sha"],
        name=f"Release {ctx.package_name} {ctx.release_version}",
        body=ctx.release_notes,
    )

    release_location_string = f"Release is at {ctx.github_release['html_url']}"
    click.secho(release_location_string)
    click.secho("CI will handle publishing the package to Rubygems.")

    ctx.github.create_pull_request_comment(
        ctx.upstream_repo, ctx.release_pr["number"], release_location_string
    )

    ctx.github.update_pull_labels(
        ctx.release_pr, add=["autorelease: tagged"], remove=["autorelease: pending"]
    )


def kokoro_job_name(upstream_repo: str, package_name: str) -> Union[str, None]:
    """Return the Kokoro job name.

    Args:
        upstream_repo (str): The GitHub repo in the form of `<owner>/<repo>`
        package_name (str): The name of package to release

    Returns:
        The name of the Kokoro job to trigger or None if there is no job to trigger
    """
    if "google-cloud-ruby" in upstream_repo:
        return f"cloud-devrel/client-libraries/google-cloud-ruby/release"
    elif "google-api-ruby-client" in upstream_repo:
        return f"cloud-devrel/client-libraries/google-api-ruby-client/release/{package_name}"
    else:
        return f"cloud-devrel/client-libraries/{package_name}/release"


def tag(ctx: TagContext = None) -> TagContext:
    if not ctx:
        ctx = TagContext()

    if ctx.interactive:
        click.secho(
            f"o/ Hey, {getpass.getuser()}, let's tag a Ruby release!", fg="magenta"
        )

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
    ctx.kokoro_job_name = kokoro_job_name(ctx.upstream_repo, ctx.package_name)

    releasetool.commands.common.publish_via_kokoro(ctx)

    if ctx.interactive:
        click.secho("\\o/ All done!", fg="magenta")

    branch = ctx.release_pr["head"]["ref"]

    try:
        ctx.github.delete_branch(repository=ctx.upstream_repo, branch=branch)
        click.secho(f"Deleted branch {branch}")
    # If user has already deleted the branch, this will fail.
    except HTTPError as exc:
        if exc.response.status_code != 422:
            click.secho(f"{exc!r}")

    return ctx
