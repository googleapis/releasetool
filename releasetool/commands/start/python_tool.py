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
import datetime

import click
from dateutil import tz

import releasetool.commands.start.python
from releasetool.commands.start.python import Context


def determine_last_release(ctx: Context) -> None:
    click.secho("> Figuring out what the last release was.", fg="cyan")
    tags = releasetool.git.list_tags()
    import pdb; pdb.set_trace()
    # releases previously looked like synthtool-2019.10.17
    # going forward, the format will be v2019.10.17
    candidates = [tag for tag in tags if tag.startswith("v") or tag.startswith(ctx.origin_repo.split('/')[1])]

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


def determine_release_version(ctx: Context) -> None:
    ctx.release_version = (
        datetime.datetime.now(datetime.timezone.utc)
        .astimezone(tz.gettz("US/Pacific"))
        .strftime("%Y.%m.%d")
    )

    if ctx.release_version in ctx.last_release_version:
        click.secho(
            f"The release version {ctx.release_version} is already used.", fg="red"
        )
        ctx.release_version = click.prompt("Please input another version: ")

    click.secho(f"Releasing {ctx.release_version}.")


def start() -> None:
    # Python tools use calver, otherwise the process is the same as python
    # libraries.
    ctx = Context()

    click.secho(f"o/ Hey, {getpass.getuser()}, let's release some stuff!", fg="magenta")

    releasetool.commands.common.setup_github_context(ctx)
    releasetool.commands.start.python.determine_package_name(ctx)
    determine_last_release(ctx)
    releasetool.commands.start.python.gather_changes(ctx)
    releasetool.commands.common.edit_release_notes(ctx)
    determine_release_version(ctx)
    releasetool.commands.start.python.create_release_branch(ctx)
    releasetool.commands.start.python.update_changelog(ctx)
    releasetool.commands.start.python.update_setup_py(ctx)
    releasetool.commands.start.python.create_release_commit(ctx)
    releasetool.commands.start.python.push_release_branch(ctx)
    # TODO: Confirm?
    releasetool.commands.start.python.create_release_pr(ctx)

    click.secho(f"\\o/ All done!", fg="magenta")
