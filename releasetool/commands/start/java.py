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

import copy
import getpass
import os
import textwrap
from typing import List, Optional

import attr
import click
import re

import releasetool.filehelpers
import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common

VERSION_REGEX = re.compile(r"(\d+)\.(\d+)\.(\d+)(-\w+)?(-\w+)?")
VERSION_UPDATE_MARKER = re.compile(r"\{x-version-update:([^:]+):([^}]+)\}")
VERSION_UPDATE_START_MARKER = re.compile(r"\{x-version-update-start:([^:]+):([^}]+)\}")
VERSION_UPDATE_END_MARKER = re.compile(r"\{x-version-update-end\}")
RELEASE_TAG_REGEX = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")


class Version:
    major: str = None
    minor: str = None
    patch: str = None
    variant: str = ""
    snapshot: bool = False

    def __init__(self, version_str):
        match = VERSION_REGEX.match(version_str)
        self.major = int(match.group(1))
        self.minor = int(match.group(2))
        self.patch = int(match.group(3))
        qualifier1 = match.group(4)
        qualifier2 = match.group(5)
        if qualifier1 and qualifier2:
            if qualifier2 == "-SNAPSHOT":
                self.variant = qualifier1
                self.snapshot = True
            else:
                self.variant = qualifier1 + qualifier2
        elif qualifier1:
            if qualifier1 == "-SNAPSHOT":
                self.snapshot = True
            else:
                self.variant = qualifier1

    def bump(self, bump_type):
        if bump_type == "minor":
            self.bump_minor()
            self.set_snapshot(False)
        elif bump_type == "patch":
            self.bump_patch()
            self.set_snapshot(False)
        elif bump_type == "snapshot":
            self.bump_patch()
            self.set_snapshot(True)
        else:
            raise ValueError("invalid bump_type: {}".format(bump_type))

    def bump_minor(self):
        self.minor += 1
        self.patch = 0

    def bump_patch(self):
        self.patch += 1

    def set_snapshot(self, snapshot):
        self.snapshot = snapshot

    def __str__(self) -> str:
        mmp = "{}.{}.{}".format(self.major, self.minor, self.patch)
        postfix = self.variant
        if self.snapshot:
            postfix += "-SNAPSHOT"
        return mmp + postfix


class ArtifactVersions:
    module: str = None
    current: Version = None
    released: Version = None

    def __init__(self, version_line=str):
        (self.module, released_version_str, current_version_str) = version_line.split(
            ":"
        )
        self.current = Version(current_version_str)
        self.released = Version(released_version_str)

    def bump(self, bump_type=str) -> None:
        if bump_type == "snapshot":
            self.next_snapshot()
        else:
            self.next_release(bump_type)

    def next_snapshot(self) -> None:
        self.current = copy.deepcopy(self.released)
        self.current.bump_patch()
        self.current.set_snapshot(True)

    def next_release(self, bump_type=str) -> None:
        self.released.bump(bump_type)
        self.current = copy.deepcopy(self.released)

    def __str__(self) -> str:
        return "{}:{}:{}".format(self.module, self.released, self.current)


@attr.s(auto_attribs=True, slots=True)
class Context(releasetool.commands.common.GitHubContext):
    last_release_version: Optional[str] = None
    last_release_committish: Optional[str] = None
    release_version: Optional[str] = None
    release_branch: Optional[str] = None
    release_type: str = None
    pull_request: Optional[dict] = None
    updated_files: List[str] = []
    versions: List[ArtifactVersions] = None


def determine_release_type(ctx: Context) -> None:
    ctx.release_type = click.prompt(
        "What type of release is this? (minor|patch|snapshot)",
        type=click.Choice(["minor", "patch", "snapshot"]),
        default="minor",
    )


def read_versions(ctx: Context) -> None:
    click.secho("> Figuring out the current version(s)", fg="cyan")

    versions = []
    with open("versions.txt") as f:
        for line in f:
            version_line = line.strip()
            if not version_line or version_line.startswith("#"):
                continue

            versions.append(ArtifactVersions(version_line))

    ctx.versions = versions


def bump_versions(ctx: Context) -> None:
    for versions in ctx.versions:
        versions.bump(ctx.release_type)


def update_versions(ctx: Context) -> None:
    if click.confirm("Bump versions?", default=True):
        with open("versions.txt", "w") as f:
            f.write("# Format:\n")
            f.write("# module:released-version:current-version\n\n")
            for versions in ctx.versions:
                f.write("{}\n".format(versions))


def replace_versions(ctx: Context) -> None:
    if click.confirm("Update versions in pom.xml files?", default=True):
        updated_files = []
        for root, _, files in os.walk("."):
            for filename in files:
                filepath = root + os.sep + filename
                if filename == "README.md" or filename == "pom.xml":
                    replace_version_in_file(ctx.versions, filepath)
                    updated_files.append(filepath)
        ctx.updated_files = updated_files


def replace_version_in_file(versions: List[ArtifactVersions], target: str):
    newlines = []
    version_map = {}
    for av in versions:
        version_map[av.module] = av

    repl_open, repl_thisline = False, False
    with open(target) as f:
        # do something
        for line in f:
            repl_thisline = repl_open
            match = VERSION_UPDATE_MARKER.search(line)
            if match:
                module_name, version_type = match.group(1), match.group(2)
                repl_thisline = True
            else:
                match = VERSION_UPDATE_START_MARKER.search(line)
                if match:
                    module_name, version_type = match.group(1), match.group(2)
                    repl_open, repl_thisline = True, True
                else:
                    match = VERSION_UPDATE_END_MARKER.search(line)
                    if match:
                        repl_open, repl_thisline = False, False

            if repl_thisline:
                if module_name not in version_map:
                    raise ValueError(
                        "module not found in version.txt: {}".format(module_name)
                    )
                module = version_map[module_name]
                new_version = None
                if version_type == "current":
                    new_version = module.current
                elif version_type == "released":
                    new_version = module.released
                else:
                    raise ValueError("invalid version type: {}".format(version_type))

                newline = re.sub(VERSION_REGEX, str(new_version), line)
                newlines.append(newline)
            else:
                newlines.append(line)

            if not repl_open:
                module_name, version_type = "", ""

    with open(target, "w") as f:
        for line in newlines:
            f.write(line)


def determine_package_name(ctx: Context) -> None:
    click.secho("> Figuring out the package name.", fg="cyan")
    ctx.package_name = os.path.basename(os.getcwd())
    click.secho(f"Looks like we're releasing {ctx.package_name}.")


def determine_last_release(ctx: Context) -> None:
    click.secho("> Figuring out what the last release was.", fg="cyan")
    tags = releasetool.git.list_tags()
    candidates = [tag for tag in tags if RELEASE_TAG_REGEX.match(tag)]

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
        ctx.last_release_version = click.prompt("Last version", default="0.0.0")

    click.secho(f"The last release was {ctx.last_release_version}.")


def gather_changes(ctx: Context) -> None:
    click.secho(f"> Gathering changes since {ctx.last_release_version}", fg="cyan")
    ctx.changes = releasetool.git.summary_log(
        from_=ctx.last_release_committish, to=f"{ctx.upstream_name}/master"
    )
    ctx.changes = [
        ctx.github.link_pull_request(c, ctx.upstream_repo) for c in ctx.changes
    ]
    click.secho(f"Cool, {len(ctx.changes)} changes found.")


def determine_release_version(ctx: Context) -> None:
    click.secho(f"> Now it's time to pick a release version!", fg="cyan")
    release_notes = textwrap.indent(ctx.release_notes, "\t")
    click.secho(f"Here's the release notes you wrote:\n\n{release_notes}\n")

    release_version = Version(ctx.last_release_version)
    release_version.bump(ctx.release_type)

    ctx.release_version = str(release_version)
    click.secho(f"Got it, releasing {ctx.release_version}.")


def create_release_branch(ctx: Context) -> None:
    """Create a release commit."""
    if click.confirm("Create release branch?", default=True):
        ctx.release_branch = f"release-{ctx.package_name}-v{ctx.release_version}"
        click.secho(f"> Creating branch {ctx.release_branch}", fg="cyan")
        releasetool.git.checkout_create_branch(ctx.release_branch)

        click.secho("> Committing changes", fg="cyan")
        message = (
            "Bump next snapshot"
            if ctx.release_type == "snapshot"
            else f"Release v{ctx.release_version}"
        )
        releasetool.git.commit(
            ["README.md", "versions.txt"] + ctx.updated_files, message
        )

        click.secho("> Pushing release branch.", fg="cyan")
        releasetool.git.push(ctx.release_branch)


def create_release_pr(ctx: Context) -> None:
    if ctx.release_branch is not None and click.confirm("Create PR?", default=True):
        click.secho(f"> Creating release pull request.", fg="cyan")

        if ctx.upstream_repo == ctx.origin_repo:
            head = ctx.release_branch
        else:
            head = f"{ctx.origin_user}:{ctx.release_branch}"

        body = (
            "This pull request was generated using releasetool.\n\n" + ctx.release_notes
        )

        title = (
            "Bump next snapshot"
            if ctx.release_type == "snapshot"
            else f"Release {ctx.package_name} v{ctx.release_version}"
        )

        ctx.pull_request = ctx.github.create_pull_request(
            ctx.upstream_repo, head=head, title=title, body=body
        )
        click.secho(f"Pull request is at {ctx.pull_request['html_url']}.")


def start() -> None:
    ctx = Context()

    # setup
    click.secho(f"o/ Hey, {getpass.getuser()}, let's release some stuff!", fg="magenta")
    releasetool.commands.common.setup_github_context(ctx)
    determine_package_name(ctx)
    determine_release_type(ctx)

    # version management in code
    read_versions(ctx)
    bump_versions(ctx)
    update_versions(ctx)
    replace_versions(ctx)

    # create release
    determine_last_release(ctx)
    if ctx.release_type == "snapshot":
        ctx.release_notes = "Bump snapshot"
    else:
        gather_changes(ctx)
        releasetool.commands.common.edit_release_notes(ctx)
    determine_release_version(ctx)
    create_release_branch(ctx)
    create_release_pr(ctx)

    click.secho(f"\o/ All done!", fg="magenta")
