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
import subprocess
import tempfile
import click

import releasetool.circleci
import releasetool.git
import releasetool.github
import releasetool.secrets
import releasetool.commands.common
from releasetool.commands.common import TagContext


def _parse_release_tag(output: str) -> str:
    match = re.search("creating release (v.*)", output)
    if match:
        return match[1]
    return None


def tag(ctx: TagContext = None) -> TagContext:
    if not ctx:
        ctx = TagContext()

    if ctx.interactive:
        click.secho(f"o/ Hey, {getpass.getuser()}, let's tag a release!", fg="magenta")

    if ctx.github is None:
        releasetool.commands.common.setup_github_context(ctx)

    # delegate releaase tagging to release-please
    default_branch = ctx.release_pr["base"]["ref"]
    repo = ctx.release_pr["base"]["repo"]["full_name"]

    with tempfile.NamedTemporaryFile("w+") as fp:
        fp.write(ctx.token)
        token_file = fp.name

        output = subprocess.check_output(
            [
                "npx",
                "release-please",
                "github-release",
                f"--token={token_file}",
                f"--default-branch={default_branch}",
                "--release-type=java-yoshi",
                "--bump-minor-pre-major=true",
                f"--repo-url={repo}",
                "--package-name=",
            ]
        )

    ctx.release_tag = _parse_release_tag(output.decode("utf-8"))
    print(ctx.release_tag)

    repo_short_name = ctx.upstream_repo.split("/")[-1]
    ctx.kokoro_job_name = (
        f"cloud-devrel/client-libraries/java/{repo_short_name}/release/stage"
    )

    if ctx.interactive:
        click.secho("\\o/ All done!", fg="magenta")

    return ctx
