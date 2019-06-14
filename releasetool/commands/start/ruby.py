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
from typing import Optional
from typing import Sequence

import attr
import click
import datetime
import glob

import releasetool.filehelpers
import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common


_CHANGELOG_TEMPLATE = """\
# Release History

[RubyGems.org history][1]

[1]: https://rubygems.org/gems/{package_name}/versions

"""


@attr.s(auto_attribs=True, slots=True)
class Context(releasetool.commands.common.GitHubContext):
    tags: Optional[Sequence[str]] = None
    last_release_version: Optional[str] = None
    last_release_committish: Optional[str] = None
    release_version: Optional[str] = None
    release_branch: Optional[str] = None
    pull_request: Optional[dict] = None
    version_file: Optional[str] = None


def determine_package_name(ctx: Context) -> None:
    click.secho("> Figuring out the package name.", fg="cyan")
    ctx.package_name = os.path.basename(os.getcwd())
    click.secho(f"Looks like we're releasing {ctx.package_name}.")


def gather_tags(ctx: Context) -> None:
    click.secho("> Figuring out what the last release was.", fg="cyan")
    ctx.tags = releasetool.git.list_tags()


def determine_last_release(ctx: Context) -> None:
    candidates = [tag for tag in ctx.tags if tag.startswith(ctx.package_name + "/")]
    if candidates and ctx.package_name in candidates[0]:
        ctx.last_release_committish = candidates[0]
        ctx.last_release_version = candidates[0].rsplit("/").pop().lstrip("v")
    elif ("google-cloud" not in ctx.package_name) and ctx.tags:
        ctx.last_release_committish = ctx.tags[0]
        ctx.last_release_version = ctx.tags[0].rsplit("/")[-1].lstrip("v")
    else:
        click.secho(
            f"I couldn't figure out the last release for {ctx.package_name}, "
            "so I'm assuming this is the first release. Can you tell me "
            "which git rev/sha to start the changelog at?",
            fg="yellow",
        )
        ctx.last_release_committish = click.prompt("Committish")
        ctx.last_release_version = "0.0.0"

    click.secho(f"The last_release committish was {ctx.last_release_committish}")
    click.secho(f"The last release version was {ctx.last_release_version}")


def gather_changes(ctx: Context) -> None:
    click.secho(f"> Gathering changes since {ctx.last_release_version}", fg="cyan")
    ctx.changes = releasetool.git.summary_log(
        from_=ctx.last_release_committish,
        to=f"{ctx.upstream_name}/master",
        format="%s%n%b%n",
    )
    click.secho(f"Cool, {len(ctx.changes)} changes found.")


def edit_release_notes(ctx: Context) -> None:
    click.secho(f"> Opening your editor to finalize release notes.", fg="cyan")
    release_notes = "\n".join(change.strip() for change in ctx.changes)
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


def update_changelog(ctx: Context) -> None:
    changelog_filename = "CHANGELOG.md"
    click.secho(f"> Updating {changelog_filename}.", fg="cyan")

    if not os.path.exists(changelog_filename):
        print(f"{changelog_filename} does not yet exist. Opening it for " "creation.")

        releasetool.filehelpers.open_editor_with_content(
            changelog_filename,
            _CHANGELOG_TEMPLATE.format(package_name=ctx.package_name),
        )

    today = datetime.date.today()
    changelog_entry = (
        f"### {ctx.release_version} / {today}" f"\n\n" f"{ctx.release_notes}" f"\n\n"
    )
    releasetool.filehelpers.insert_before(
        changelog_filename, changelog_entry, r"^### (.+)$|\Z"
    )


def update_version(ctx: Context) -> None:
    click.secho("> Updating version.rb.", fg="cyan")
    gemspec = glob.glob("*.gemspec")[0]
    version = releasetool.filehelpers.extract(gemspec, r"gem.version.*=(.*)")
    if version.lower().find("version") == -1:
        final = (
            releasetool.filehelpers.extract(gemspec, "(gem.version.*=)")
            + f' "{ctx.release_version}"'
        )
        ctx.version_file = gemspec
        releasetool.filehelpers.replace(ctx.version_file, r"gem.version.*", final)
    else:
        ctx.version_file = glob.glob("lib/**/version.rb", recursive=True)[0]
        releasetool.filehelpers.replace(
            ctx.version_file, r'VERSION = "(.+?)"', f'VERSION = "{ctx.release_version}"'
        )


def create_release_commit(ctx: Context) -> None:
    """Create a release commit."""
    click.secho("> Committing changes to CHANGELOG.md, {ctx.version_file}", fg="cyan")
    releasetool.git.commit(
        ["CHANGELOG.md", ctx.version_file],
        f"Release {ctx.package_name} {ctx.release_version}\n\n{ctx.release_notes}",
    )


def push_release_branch(ctx: Context) -> None:
    click.secho("> Pushing release branch.", fg="cyan")
    releasetool.git.push(ctx.release_branch)


def create_release_pr(ctx: Context, autorelease: bool = True) -> None:
    click.secho(f"> Creating release pull request.", fg="cyan")

    if ctx.upstream_repo == ctx.origin_repo:
        head = ctx.release_branch
    else:
        head = f"{ctx.origin_user}:{ctx.release_branch}"

    log = releasetool.git.log(
        from_=ctx.last_release_committish, to=f"{ctx.upstream_name}/master"
    )
    log_html = f"<details><summary>Commits since previous release</summary><pre><code>{log}</code></pre></details>"
    diff = releasetool.git.diff(
        from_=ctx.last_release_committish, to=f"{ctx.upstream_name}/master"
    )
    diff_html = f"<details><summary>Code changes since previous release</summary>\n\n```diff\n{diff}\n```\n\n</details>"

    ctx.pull_request = ctx.github.create_pull_request(
        ctx.upstream_repo,
        head=head,
        title=f"Release {ctx.package_name} {ctx.release_version}",
        body=f"{ctx.release_notes}\n\n{log_html}\n\n{diff_html}\n\nThis pull request was generated using releasetool.",
    )

    if autorelease:
        ctx.github.add_issue_labels(
            ctx.upstream_repo, ctx.pull_request["number"], ["autorelease: pending"]
        )

    click.secho(f"Pull request is at {ctx.pull_request['html_url']}.")


def checkout_master() -> None:
    click.secho("> Checkout master branch.", fg="cyan")
    releasetool.git.checkout_branch("master")


def start() -> None:
    ctx = Context()

    click.secho(f"o/ Hey, {getpass.getuser()}, let's release some Ruby!", fg="magenta")

    releasetool.commands.common.setup_github_context(ctx)
    determine_package_name(ctx)
    gather_tags(ctx)
    determine_last_release(ctx)
    gather_changes(ctx)
    edit_release_notes(ctx)
    determine_release_version(ctx)
    create_release_branch(ctx)
    update_changelog(ctx)
    update_version(ctx)
    create_release_commit(ctx)
    push_release_branch(ctx)
    # TODO: Confirm?
    create_release_pr(ctx)
    checkout_master()

    click.secho(f"\\o/ All done!", fg="magenta")
