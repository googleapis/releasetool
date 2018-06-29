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

import click

from releasetool.commands.tag import python


def get_release_notes(ctx: python.Context) -> None:
    click.secho("> Grabbing the release notes.")
    changelog = ctx.github.get_contents(
        ctx.github_repo,
        f'CHANGELOG.md',
        ref=ctx.release_pr['merge_commit_sha'])
    changelog = changelog.decode('utf-8')

    match = re.search(
        rf'## {ctx.release_version}\n(?P<notes>.+?)(\n##\s|\Z)',
        changelog, re.DOTALL | re.MULTILINE)
    if match is not None:
        ctx.release_notes = match.group('notes').strip()
    else:
        ctx.release_notes = ''


def create_release(ctx: python.Context) -> None:
    click.secho("> Creating the release.")

    ctx.github_release = ctx.github.create_release(
        repository=ctx.github_repo,
        tag_name=ctx.release_tag,
        target_committish=ctx.release_pr['merge_commit_sha'],
        name=f'{ctx.package_name} {ctx.release_version}',
        body=ctx.release_notes)

    release_location_string = f"Release is at {ctx.github_release['html_url']}"
    click.secho(release_location_string)

    ctx.github.create_pull_request_comment(
        ctx.github_repo, ctx.release_pr['number'], release_location_string)


def publish_to_pypi(ctx: python.Context) -> None:
    # TODO: Replace this with Kokoro!
    click.secho("> Publishing to PyPI.")
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    for path in glob.glob('*.egg-info'):
        shutil.rmtree('path', ignore_errors=True)
    subprocess.check_output(['python3', 'setup.py', 'sdist', 'bdist_wheel'])
    dists = glob.glob('dist/*')
    subprocess.check_call(['twine', 'upload'] + dists)


def tag() -> None:
    ctx = python.Context()

    click.secho(
        f"o/ Hey, {getpass.getuser()}, let's tag a release!",
        fg='magenta')

    python.setup_context(ctx)

    python.determine_release_pr(ctx)
    python.determine_release_tag(ctx)
    python.determine_package_name_and_version(ctx)
    get_release_notes(ctx)

    create_release(ctx)

    publish_to_pypi(ctx)

    click.secho(f"\o/ All done!", fg='magenta')
