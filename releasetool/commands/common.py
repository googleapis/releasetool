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

from typing import Sequence

import attr
import click

import releasetool.git
import releasetool.github
import releasetool.secrets


@attr.s(auto_attribs=True, slots=True)
class GitHubContext:
    github: releasetool.github.GitHub = None
    origin_user: str = None
    origin_repo: str = None
    upstream_repo: str = None
    package_name: str = None


def _determine_origin(ctx: GitHubContext) -> None:
    remotes = releasetool.git.get_github_remotes()
    origin = remotes['origin']
    ctx.origin_user = origin.split('/')[0]
    ctx.origin_repo = origin


def _determine_upstream(ctx: GitHubContext, owners: Sequence[str]) -> None:
    remotes = releasetool.git.get_github_remotes()
    repos = [
        name for remote, name in remotes.items()
        if name.lower().startswith(owners)]

    if not repos:
        raise ValueError('Unable to determine the upstream GitHub repo. :(')

    ctx.upstream_repo = repos.pop()


def setup_github_context(
        ctx: GitHubContext,
        owners: Sequence[str] = ('googlecloudplatform', 'googleapis')) -> None:
    click.secho('> Determining GitHub context.', fg='cyan')
    github_token = releasetool.secrets.ensure_password(
        'github',
        'Please provide your GitHub API token with write:repo_hook and '
        'public_repo (https://github.com/settings/tokens)')
    ctx.github = releasetool.github.GitHub(github_token)

    _determine_origin(ctx)
    _determine_upstream(ctx, owners)

    click.secho(f'Origin: {ctx.origin_repo}, Upstream: {ctx.upstream_repo}')
