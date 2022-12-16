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
from typing import List, Union

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


"""A list of repositories that have a different kokoro job location.
"""
# Standard Java Framework repos in the GoogleCloudPlatform org
java_framework_release_pool_repos: List[str] = [
    "google-cloud-spanner-hibernate",
    "spring-cloud-gcp",
    "cloud-spanner-r2dbc",
]
functions_framework_java_packages: List[str] = [
    "functions-framework-api",
    "java-function-invoker",
    "function-maven-plugin",
]


def kokoro_job_name(upstream_repo: str, package_name: str) -> Union[str, None]:
    """Return the Kokoro job name.

    Args:
        upstream_repo (str): The GitHub repo in the form of `<owner>/<repo>`
        package_name (str): The name of package to release

    Returns:
        The name of the Kokoro job to trigger or None if there is no job to trigger
    """
    repo_short_name = upstream_repo.split("/")[-1]

    if repo_short_name in java_framework_release_pool_repos:
        return f"cloud-java-frameworks/{repo_short_name}/stage"

    if (
        repo_short_name == "functions-framework-java"
        and package_name in functions_framework_java_packages
    ):
        return f"functions-framework/java/{package_name}/release"

    else:
        return f"cloud-devrel/client-libraries/java/{repo_short_name}/release/stage"


def package_name(pull: dict) -> Union[str, None]:
    if pull.__contains__("title"):
        title = pull["title"]
        match = re.search(".* release (.*) [0-9].*", title)
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

    with tempfile.NamedTemporaryFile("w+t", delete=False) as fp:
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
            "--debug",
        ]
    )

    ctx.release_tag = _parse_release_tag(output.decode("utf-8"))
    ctx.kokoro_job_name = kokoro_job_name(ctx.upstream_repo, ctx.package_name)

    if ctx.interactive:
        click.secho("\\o/ All done!", fg="magenta")

    return ctx
