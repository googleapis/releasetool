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
import glob
import re
import shutil
import subprocess
from urllib import parse

import click

import releasetool.commands.common
from releasetool.commands.tag import python


def get_release_notes(ctx: python.Context) -> None:
    click.secho("> Grabbing the release notes.")
    changelog = ctx.github.get_contents(
        ctx.upstream_repo, f"CHANGELOG.md", ref=ctx.release_pr["merge_commit_sha"]
    ).decode("utf-8")

    match = re.search(
        rf"## {ctx.release_version}\n(?P<notes>.+?)(\n##\s|\Z)",
        changelog,
        re.DOTALL | re.MULTILINE,
    )
    if match is not None:
        ctx.release_notes = match.group("notes").strip()
    else:
        ctx.release_notes = ""


def create_release(ctx: python.Context) -> None:
    click.secho("> Creating the release.")

    ctx.github_release = ctx.github.create_release(
        repository=ctx.upstream_repo,
        tag_name=ctx.release_tag,
        target_committish=ctx.release_pr["merge_commit_sha"],
        name=f"{ctx.package_name} {ctx.release_version}",
        body=ctx.release_notes,
    )

    release_location_string = f"Release is at {ctx.github_release['html_url']}"
    click.secho(release_location_string)

    ctx.github.create_pull_request_comment(
        ctx.upstream_repo, ctx.release_pr["number"], release_location_string
    )


def publish_to_pypi(ctx: python.Context) -> None:
    kokoro_url = "https://fusion.corp.google.com/projectanalysis/current/KOKORO/"
    project = f"prod:cloud-devrel/client-libraries/{ctx.package_name}/release"
    project_url = parse.urljoin(kokoro_url, parse.quote_plus(project))

    click.secho(
        f"> Trigger the Kokoro build with the commitish below to publish to PyPI.",
        fg="cyan",
    )
    click.secho(f"Build:\t\t{click.style(project_url, underline=True)}")
    click.secho(f"Commitish:\t{click.style(ctx.release_tag, bold=True)}")

    if click.confirm("Would you like to go the Kokoro build page?"):
        click.launch(project_url)


def tag() -> None:
    ctx = python.Context()

    click.secho(f"o/ Hey, {getpass.getuser()}, let's tag a release!", fg="magenta")

    releasetool.commands.common.setup_github_context(ctx)

    python.determine_release_pr(ctx)
    python.determine_release_tag(ctx)
    python.determine_package_name_and_version(ctx)
    get_release_notes(ctx)

    create_release(ctx)

    publish_to_pypi(ctx)

    click.secho(f"\o/ All done!", fg="magenta")
