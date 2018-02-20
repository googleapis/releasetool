import click

import releasetool.commands.start.python
import releasetool.commands.tag.python


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        return ctx.invoke(start)


@main.command()
def start():
    releasetool.commands.start.python.start()


@main.command()
def tag():
    releasetool.commands.tag.python.tag()
