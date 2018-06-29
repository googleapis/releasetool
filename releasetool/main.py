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

import click

import releasetool.commands.start.python
import releasetool.commands.start.python_tool
import releasetool.commands.start.nodejs
import releasetool.commands.tag.python
import releasetool.commands.tag.python_tool
import releasetool.commands.tag.nodejs


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        return ctx.invoke(start)


_language_choices = ['python', 'python-tool', 'nodejs']
_language_option = click.option(
    '--language',
    prompt=f"Which language ({', '.join(_language_choices)})?",
    type=click.Choice(_language_choices))


@main.command()
@_language_option
def start(language):
    if language == 'python':
        return releasetool.commands.start.python.start()
    if language == 'python-tool':
        return releasetool.commands.start.python_tool.start()
    if language == 'nodejs':
        return releasetool.commands.start.nodejs.start()


@main.command()
@_language_option
def tag(language):
    if language == 'python':
        return releasetool.commands.tag.python.tag()
    if language == 'python-tool':
        return releasetool.commands.tag.python_tool.tag()
    if language == 'nodejs':
        return releasetool.commands.tag.nodejs.tag()
