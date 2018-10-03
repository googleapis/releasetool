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
import sys
from typing import Optional

import attr
import click

import releasetool.git


@attr.s(auto_attribs=True, slots=True)
class Context:
    release_tag: Optional[str] = None


def determine_release_tag(ctx: Context) -> None:
    click.secho("> Determining what the release tag should be.", fg="cyan")
    title = releasetool.git.get_commit_title("origin/master")
    regexp = "Release (.+)"
    match = re.match(regexp, title)
    if match is None:
        print(
            f"The title of the commit at origin/master doesn't match '{regexp}'.\n"
            "You need to:\n"
            "1. Run 'releasetool start' to create a release CL.\n"
            "2. Get it reviewed and submit it.\n"
            "3. Run 'git pull' on master to sync your local repo."
            )
        sys.exit(1)
    ctx.release_tag = "v" + match.group(1)
    click.secho(f"Release tag is {ctx.release_tag}.")

def tag() -> None:
    ctx = Context()
    click.secho(f"o/ Hey, {getpass.getuser()}, let's tag a release!", fg="magenta")
    determine_release_tag(ctx)
    releasetool.git.tag(ctx.release_tag, "origin/master")
    print(f"Tagged origin/master with {ctx.release_tag}.")
    if click.confirm("Push the tag?"):
        releasetool.git.push_tag(ctx.release_tag)
    click.secho(f"\o/ All done!", fg="magenta")
