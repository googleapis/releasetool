import getpass
import re

import attr
import click

import releasetool.git
import releasetool.github
import releasetool.secrets


@attr.s(auto_attribs=True, slots=True)
class Context:
    github: releasetool.github.GitHub = None
    github_repo: str = None
    package_name: str = None
    release_pr: dict = None
    release_tag: str = None
    release_version: str = None
    release_notes: str = None
    github_release: dict = None


def setup_context(ctx: Context) -> None:
    click.secho('> Determining basic context.', fg='cyan')
    github_token = releasetool.secrets.get_password('github')
    ctx.github = releasetool.github.GitHub(github_token)
    ctx.github_repo = releasetool.git.get_github_repo_name()
    click.secho(f'GitHub Repo: {ctx.github_repo}')


def determine_release_pr(ctx: Context) -> None:
    click.secho(
        "> Let's figure out which pull request corresponds to your release.",
        fg='cyan')

    pulls = ctx.github.list_pull_requests(ctx.github_repo, state='closed')
    pulls = [pull for pull in pulls if 'release' in pull['title'].lower()][:10]

    click.secho('> Please pick one of the following PRs:\n')
    for n, pull in enumerate(pulls, 1):
        print(f"\t{n}: {pull['title']}")

    pull_idx = click.prompt(
        '\nWhich one do you want to tag and release?', type=int)

    ctx.release_pr = pulls[pull_idx-1]


def determine_release_tag(ctx: Context) -> None:
    click.secho(
        "> Determining what the release tag should be.",
        fg='cyan')
    head_ref = ctx.release_pr['head']['ref']
    match = re.match('release-(.+)', head_ref)

    if match is not None:
        ctx.release_tag = match.group(1)
    else:
        print(
            "I couldn't determine what the release tag should be from the PR's"
            f"head ref {head_ref}.")
        ctx.release_tag = click.prompt(
            'What should the release tag be (for example, storage-1.2.3)?')

    click.secho(f"Release tag is {ctx.release_tag}.")


def determine_package_name_and_version(ctx: Context) -> None:
    click.secho(
        "> Determining the package name and version.",
        fg='cyan')
    match = re.match(
        '(?P<name>.+?)-(?P<version>\d+?\.\d+?\.\d+?)', ctx.release_tag)
    ctx.package_name = match.group('name')
    ctx.release_version = match.group('version')
    click.secho(
        f"Package name: {ctx.package_name}, "
        "package version: {ctx.release_version}.")


def get_release_notes(ctx: Context) -> None:
    click.secho("> Grabbing the release notes.")
    changelog = ctx.github.get_contents(
        ctx.github_repo,
        f'{ctx.package_name}/CHANGELOG.md',
        ref=ctx.release_pr['merge_commit_sha'])
    changelog = changelog.decode('utf-8')

    match = re.search(
        rf'## {ctx.release_version}\n(?P<notes>.+?)(\n##\s|\Z)',
        changelog, re.DOTALL | re.MULTILINE)
    if match is not None:
        ctx.release_notes = match.group('notes').strip()
    else:
        ctx.release_notes = ''


def create_release(ctx: Context) -> None:
    click.secho("> Creating the release.")

    ctx.github_release = ctx.github.create_release(
        repository=ctx.github_repo,
        tag_name=ctx.release_tag,
        target_committish=ctx.release_pr['merge_commit_sha'],
        name=f'google-cloud-{ctx.package_name} {ctx.release_version}',
        body=ctx.release_notes)

    click.secho(f"Release is at {ctx.github_release['html_url']}.")
    click.secho("CI will handle publishing the package to PyPI.")


def tag() -> None:
    ctx = Context()

    click.secho(
        f"o/ Hey, {getpass.getuser()}, let's tag a release!",
        fg='magenta')

    setup_context(ctx)

    determine_release_pr(ctx)
    determine_release_tag(ctx)
    determine_package_name_and_version(ctx)
    get_release_notes(ctx)

    create_release(ctx)

    click.secho(f"\o/ All done!", fg='magenta')
