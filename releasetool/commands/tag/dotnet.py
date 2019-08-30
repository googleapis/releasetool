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

import click

import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common
from releasetool.commands.common import TagContext

from typing import List

RELEASE_LINE_PATTERN = r"- Release (.*) version (.*)"


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


def create_releases(ctx: TagContext) -> None:	
    click.secho("> Creating the release.")

    commitish = ctx.release_pr["merge_commit_sha"]
    lines = ctx.release_pr["body"].splitlines()
    pr_comment = ""
    for line in lines:
        match = re.search(RELEASE_LINE_PATTERN, line)
        if match is not None:
            package = match.group(1)
            version = match.group(2)
            tag = package + "-" + version
            release = ctx.github.create_release(
                repository=ctx.upstream_repo,
                tag_name=tag,
                target_commitish=commitish,
                name=tag
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
    ctx.kokoro_job_name = (
        f"cloud-sharp/google-cloud-dotnet/gcp_windows/autorelease"
    )
    ctx.github.update_pull_labels(
        ctx.release_pr, add=["autorelease: tagged"], remove=["autorelease: pending"]
    )
    releasetool.commands.common.publish_via_kokoro(ctx)    


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
