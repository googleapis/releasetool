import getpass
from typing import Union

import click

import releasetool.commands.tag.nodejs
from releasetool.commands.common import TagContext


def kokoro_job_name(upstream_repo: str, package_name: str) -> Union[str, None]:
    """Return the Kokoro job name.

    Args:
        upstream_repo (str): The GitHub repo in the form of `<owner>/<repo>`
        package_name (str): The name of package to release

    Returns:
        The name of the Kokoro job to trigger or None if there is no job to trigger
    """
    return None


def tag(ctx: TagContext = None) -> TagContext:
    # PHP just needs a release to be tagged on GitHub.
    # Tagging logic is the same as NodeJs.
    if not ctx:
        ctx = TagContext()

    if ctx.interactive:
        click.secho(f"o/ Hey, {getpass.getuser()}, let's tag a release!", fg="magenta")

    if ctx.github is None:
        releasetool.commands.common.setup_github_context(ctx)

    if ctx.release_pr is None:
        releasetool.commands.tag.nodejs.determine_release_pr(ctx)

    releasetool.commands.tag.nodejs.determine_release_tag(ctx)
    releasetool.commands.tag.nodejs.determine_package_version(ctx)

    # If the release already exists, don't do anything
    if releasetool.commands.common.release_exists(ctx):
        click.secho(f"{ctx.release_tag} already exists.", fg="magenta")
        return ctx

    releasetool.commands.tag.nodejs.get_release_notes(ctx)
    releasetool.commands.tag.nodejs.create_release(ctx)

    if ctx.interactive:
        click.secho("\\o/ All done!", fg="magenta")

    return ctx
