# Copyright 2019 Google LLC
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

import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common
from releasetool.commands.common import TagContext

RELEASE_LINE_PATTERN = r"^(?:- )?Release ([^ ]*) version (\d+\.\d+.\d+(-[^ ]*)?)$"


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


def create_releases(ctx: TagContext) -> None:
    click.secho("> Creating the release.")

    commitish = ctx.release_pr["merge_commit_sha"]
    title = ctx.release_pr["title"]
    body_lines = (ctx.release_pr["body"] or "").splitlines()
    all_lines = [title] + body_lines
    pr_comment = ""
    for line in all_lines:
        match = re.search(RELEASE_LINE_PATTERN, line)
        if match is not None:
            package = match.group(1)
            version = match.group(2)
            tag = package + "-" + version
            ctx.github.create_release(
                repository=ctx.upstream_repo,
                tag_name=tag,
                target_commitish=commitish,
                name=f"{package} version {version}",
                # TODO: either reformat the message as we do in TagReleases,
                # or make sure we create the PR with an "already-formatted"
                # body. (The latter is probably simpler, and will make the
                # PR easier to read anyway.)
                body=ctx.release_pr["body"],
                # Versions like "1.0.0-beta01" or "0.9.0" are prerelease
                prerelease="-" in version or version.startswith("0."),
            )
            click.secho(f"Created release for {tag}")
            pr_comment = pr_comment + f"- Created release for {tag}\n"

    if pr_comment == "":
        raise ValueError("No releases found within pull request")

    ctx.github.create_pull_request_comment(
        ctx.upstream_repo, ctx.release_pr["number"], pr_comment
    )

    # This isn't a tag, but that's okay - it just needs to be a commitish for
    # Kokoro to build against.
    ctx.release_tag = commitish

    ctx.kokoro_job_name = kokoro_job_name(ctx.upstream_repo, "")
    ctx.github.update_pull_labels(
        ctx.release_pr, add=["autorelease: tagged"], remove=["autorelease: pending"]
    )
    releasetool.commands.common.publish_via_kokoro(ctx)


def kokoro_job_name(upstream_repo: str, package_name: str) -> Union[str, None]:
    """Return the Kokoro job name.

    Args:
        upstream_repo (str): The GitHub repo in the form of `<owner>/<repo>`
        package_name (str): The name of package to release

    Returns:
        The name of the Kokoro job to trigger or None if there is no job to trigger
    """
    repo_short_name = upstream_repo.split("/")[-1]
    if repo_short_name == "dotnet-spanner-entity-framework":
        return (
            f"cloud-libraries-dotnet/{repo_short_name}/gcp_windows_docker/autorelease"
        )
    elif repo_short_name == "google-cloudevents-dotnet":
         return (
            f"cloud-libraries-dotnet/{repo_short_name}/rbe_windows_releases/autorelease"
        )
    else:
        return f"cloud-sharp/{repo_short_name}/gcp_windows/autorelease"


def package_name(pull: dict) -> Union[str, None]:
    return None


# Note: unlike other languages, the .NET libraries may need multiple
# tags for a single release PR, usually for dependent APIs, e.g.
# Google.Cloud.Spanner.Data depending on Google.Cloud.Spanner.V1.
# We create multiple releases in the create_releases function, and set
# ctx.release_tag to the commit we've tagged (as all tags will use the same commit).
def tag(ctx: TagContext = None) -> TagContext:
    if not ctx:
        ctx = TagContext()

    if ctx.interactive:
        click.secho(f"o/ Hey, {getpass.getuser()}, let's tag a release!", fg="magenta")

    if ctx.github is None:
        releasetool.commands.common.setup_github_context(ctx)

    if ctx.release_pr is None:
        determine_release_pr(ctx)

    create_releases(ctx)

    return ctx
