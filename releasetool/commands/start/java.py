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
import os
import textwrap
from typing import Collection, Optional, Sequence
from glob import glob

import attr
import click
import re

import releasetool.filehelpers
import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common


@attr.s(auto_attribs=True, slots=True)
class Context(releasetool.commands.common.GitHubContext):
    package_name: Optional[str] = None
    last_release_version: Optional[str] = None
    last_release_committish: Optional[str] = None
    changes: Sequence[str] = ()
    pom_files: Collection[str] = []
    snapshot_version: Optional[str] = None
    release_notes: Optional[str] = None
    release_version: Optional[str] = None
    release_branch: Optional[str] = None
    pull_request: Optional[dict] = None


def determine_package_name(ctx: Context) -> None:
    click.secho("> Figuring out the package name.", fg="cyan")
    ctx.package_name = os.path.basename(os.getcwd())
    click.secho(f"Looks like we're releasing {ctx.package_name}.")


def determine_last_release(ctx: Context) -> None:
    click.secho("> Figuring out what the last release was.", fg="cyan")
    tags = releasetool.git.list_tags()
    candidates = [tag for tag in tags if tag.startswith("v")]

    if candidates:
        ctx.last_release_committish = candidates[0]
        # strip the leading 'v'
        ctx.last_release_version = candidates[0].lstrip("v")

    else:
        click.secho(
            f"I couldn't figure out the last release for {ctx.package_name}, "
            "so I'm assuming this is the first release. Can you tell me "
            "which git rev/sha to start the changelog at?",
            fg="yellow",
        )
        ctx.last_release_committish = click.prompt("Committish")
        ctx.last_release_version = "0.0.0"

    click.secho(f"The last release was {ctx.last_release_version}.")


def determine_snapshot_version(ctx: Context) -> None:
    click.secho("> Figuring out the current snapshot version.", fg="cyan")

    with open("pom.xml", "r") as fh:
        content = fh.read()
        m = re.search(r"<version>(\d+\.\d+\.\d+)-SNAPSHOT</version>", content)
        if m:
            ctx.snapshot_version = m.group(1)

    if ctx.snapshot_version is None:
        click.secho(
            "I couldn't figure out the current snapshot version from pom.xml.", fg="red"
        )
        click.exit(1)


def gather_changes(ctx: Context) -> None:
    click.secho(f"> Gathering changes since {ctx.last_release_version}", fg="cyan")
    ctx.changes = releasetool.git.summary_log(
        from_=ctx.last_release_committish, to=f"{ctx.upstream_name}/master"
    )
    click.secho(f"Cool, {len(ctx.changes)} changes found.")


def edit_release_notes(ctx: Context) -> None:
    click.secho(f"> Opening your editor to finalize release notes.", fg="cyan")
    release_notes = "\n".join(f"- {change}" for change in ctx.changes)
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


def determine_release_version(ctx: Context) -> None:
    click.secho(f"> Now it's time to pick a release version!", fg="cyan")
    release_notes = textwrap.indent(ctx.release_notes, "\t")
    click.secho(f"Here's the release notes you wrote:\n\n{release_notes}\n")

    parsed_version = [int(x) for x in ctx.last_release_version.split(".")]

    if parsed_version == [0, 0, 0]:
        ctx.release_version = "0.1.0"
        return

    selection = click.prompt(
        "Is this a major, minor, or patch update (or enter the new version " "directly)"
    )
    if selection == "major":
        parsed_version[0] += 1
        parsed_version[1] = 0
        parsed_version[2] = 0
    elif selection == "minor":
        parsed_version[1] += 1
        parsed_version[2] = 0
    elif selection == "patch":
        parsed_version[2] += 1
    else:
        ctx.release_version = selection
        return

    ctx.release_version = "{}.{}.{}".format(*parsed_version)

    click.secho(f"Got it, releasing {ctx.release_version}.")


def create_release_branch(ctx) -> None:
    ctx.release_branch = f"release-{ctx.package_name}-v{ctx.release_version}"
    click.secho(f"> Creating branch {ctx.release_branch}", fg="cyan")
    return releasetool.git.checkout_create_branch(ctx.release_branch)


def gather_pom_xml_files(ctx: Context) -> None:
    ctx.pom_files = glob("**/pom.xml", recursive=True)


def update_pom_xml(ctx: Context) -> None:
    click.secho("> Updating snapshot versions in pom.xml files.", fg="cyan")
    for file in ctx.pom_files:
        click.secho(f"> Updating {file}.", fg="cyan")
        releasetool.filehelpers.replace(
            file,
            f"<version>{ctx.snapshot_version}-SNAPSHOT</version>",
            f"<version>{ctx.release_version}</version>",
        )


def update_readme(ctx: Context) -> None:
    click.secho("> Updating README.md file.", fg="cyan")
    releasetool.filehelpers.replace(
        "README.md", ctx.last_release_version, ctx.release_version
    )


def create_release_commit(ctx: Context) -> None:
    """Create a release commit."""
    click.secho("> Committing changes", fg="cyan")
    releasetool.git.commit(
        ["README.md"] + ctx.pom_files, f"Release v{ctx.release_version}"
    )


def push_release_branch(ctx: Context) -> None:
    click.secho("> Pushing release branch.", fg="cyan")
    releasetool.git.push(ctx.release_branch)


def create_release_pr(ctx: Context) -> None:
    click.secho(f"> Creating release pull request.", fg="cyan")

    if ctx.upstream_repo == ctx.origin_repo:
        head = ctx.release_branch
    else:
        head = f"{ctx.origin_user}:{ctx.release_branch}"

    body = "This pull request was generated using releasetool.\n\n" + ctx.release_notes

    ctx.pull_request = ctx.github.create_pull_request(
        ctx.upstream_repo,
        head=head,
        title=f"Release {ctx.package_name} v{ctx.release_version}",
        body=body,
    )
    click.secho(f"Pull request is at {ctx.pull_request['html_url']}.")


def start() -> None:
    ctx = Context()

    click.secho(f"o/ Hey, {getpass.getuser()}, let's release some stuff!", fg="magenta")

    releasetool.commands.common.setup_github_context(ctx)
    determine_package_name(ctx)
    determine_last_release(ctx)
    determine_snapshot_version(ctx)
    gather_changes(ctx)
    edit_release_notes(ctx)
    determine_release_version(ctx)
    create_release_branch(ctx)
    gather_pom_xml_files(ctx)
    update_pom_xml(ctx)
    create_release_commit(ctx)
    push_release_branch(ctx)
    # TODO: Confirm?
    create_release_pr(ctx)

    click.secho(f"\o/ All done!", fg="magenta")
