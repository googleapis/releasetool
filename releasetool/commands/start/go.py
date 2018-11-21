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
import getpass
import json
import os
import subprocess
import textwrap
from typing import Dict, List, Optional, Sequence

import attr
import click
from dateutil import tz

import releasetool.filehelpers
import releasetool.git


_CHANGELOG_FILENAME = "CHANGES.md"

_CHANGELOG_TEMPLATE = """\
# Changes

"""


@attr.s(auto_attribs=True, slots=True)
class Context:
    module_name: str = None
    relative_module_name: str = None  # relative to repo root; used for tags
    changes: Sequence[str] = ()
    release_notes: Optional[str] = None
    last_release_version: Optional[str] = None
    last_release_committish: Optional[str] = None
    release_version: Optional[str] = None
    release_branch: Optional[str] = None


def determine_module_name(ctx: Context) -> None:
    # Get the module name from the go.mod file in the current directory.
    click.secho("> Figuring out the module name.", fg="cyan")
    info = read_gomod()
    if info is None:
        click.secho("Looks like we're releasing the repo (no modules).")
    else:
        ctx.module_name = info["Module"]["Path"]
        ctx.relative_module_name = relative_module_name(ctx.module_name)
        click.secho(
            f"Looks like we're releasing {ctx.module_name} (relative path {ctx.relative_module_name})."
        )


def read_gomod() -> Optional[dict]:
    if os.path.isfile("go.mod"):
        output = subprocess.check_output(["go", "mod", "edit", "-json"]).decode("utf-8")
        return json.loads(output)
    elif os.path.isdir(".git"):
        return None
    else:
        raise ValueError("no go.mod; must release from repo root")


def relative_module_name(modname) -> str:
    """Returns modname relative to the repo root.

    Assumes modname's go.mod file is in the current directory.
    """
    dir = os.getcwd()
    components: List[str] = []
    while dir != "/":
        if os.path.isdir(os.path.join(dir, ".git")):
            return "/".join(reversed(components))
        dir, c = os.path.split(dir)
        components.append(c)
    raise ValueError("not inside a git repo")


def determine_last_release(ctx: Context) -> None:
    click.secho("> Figuring out what the last release was.", fg="cyan")
    if ctx.relative_module_name is None:
        prefix = "v"
    else:
        prefix = ctx.relative_module_name + "/v"
    tags = releasetool.git.list_tags()
    candidates = [tag for tag in tags if tag.startswith(prefix)]

    if candidates:
        ctx.last_release_committish = candidates[0]
        ctx.last_release_version = candidates[0].rsplit("/").pop()[1:]

    else:
        click.secho(
            f"I couldn't figure out the last release for {ctx.module_name}, "
            "so I'm assuming this is the first release. Can you tell me "
            "which git rev/sha to start the changelog at?",
            fg="yellow",
        )
        ctx.last_release_committish = click.prompt("Committish")
        ctx.last_release_version = "0.0.0"

    click.secho(f"The last release was {ctx.last_release_version}.")


def gather_changes(ctx: Context) -> None:
    click.secho(f"> Gathering changes since {ctx.last_release_version}", fg="cyan")
    ctx.changes = releasetool.git.summary_log(
        from_=ctx.last_release_committish, to=f"origin/master"
    )
    click.secho(f"Cool, {len(ctx.changes)} changes found.")


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
    if ctx.module_name is None:
        ctx.release_branch = f"release-{ctx.release_version}"
    else:
        ctx.release_branch = f"release-{ctx.module_name}-{ctx.release_version}"
    click.secho(f"> Creating branch {ctx.release_branch}", fg="cyan")
    return releasetool.git.checkout_create_branch(ctx.release_branch)


def update_changelog(ctx: Context) -> None:
    click.secho(f"> Updating {_CHANGELOG_FILENAME}.", fg="cyan")

    if not os.path.exists(_CHANGELOG_FILENAME):
        print(f"{_CHANGELOG_FILENAME} does not yet exist. Opening it for creation.")

        releasetool.filehelpers.open_editor_with_content(
            _CHANGELOG_FILENAME, _CHANGELOG_TEMPLATE
        )

    changelog_entry = (
        f"## v{ctx.release_version}" f"\n\n" f"{ctx.release_notes}" f"\n\n"
    )
    releasetool.filehelpers.insert_before(
        _CHANGELOG_FILENAME, changelog_entry, r"^## (.+)$|\Z"
    )


def create_release_commit(ctx: Context) -> None:
    """Create a release commit."""
    click.secho("> Comitting changes", fg="cyan")
    releasetool.git.commit([_CHANGELOG_FILENAME], f"all: release {ctx.release_version}")


def create_release_cl(ctx: Context) -> None:
    click.secho(f"> Creating release CL.", fg="cyan")
    revs = click.prompt("reviewers (comma-separated)", default="deklerk,jba")
    subprocess.check_output(["git", "codereview", "mail", "-r", revs, "HEAD"])


def edit_release_notes(ctx: Context) -> None:
    click.secho(f"> Opening your editor to finalize release notes.", fg="cyan")
    release_notes = (
        datetime.datetime.now(datetime.timezone.utc)
        .astimezone(tz.gettz("US/Pacific"))
        .strftime("%m-%d-%Y %H:%M %Z\n\n")
    )

    packages: Dict[str, List[str]] = {}
    for change in ctx.changes:
        package, commit = change.split(":", 1)
        commit = commit.strip()
        try:
            packages[package].append(commit)
        except KeyError:
            packages[package] = [commit]

    # sort packages alphabetically
    sorted_packages = sorted(list(packages.items()), key=lambda x: x[0])
    for package, commits in sorted_packages:
        commit_list = "\n".join(f"  - {commit}" for commit in commits)
        release_notes += f"- {package}:\n{commit_list}\n"

    ctx.release_notes = releasetool.filehelpers.open_editor_with_tempfile(
        release_notes, "release-notes.md"
    ).strip()


def start() -> None:
    ctx = Context()

    click.secho(f"o/ Hey, {getpass.getuser()}, let's release some stuff!", fg="magenta")

    determine_module_name(ctx)
    determine_last_release(ctx)
    gather_changes(ctx)
    edit_release_notes(ctx)
    determine_release_version(ctx)
    create_release_branch(ctx)
    update_changelog(ctx)
    create_release_commit(ctx)
    create_release_cl(ctx)

    click.secho(f"\\o/ All done!", fg="magenta")
