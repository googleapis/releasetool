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

import functools
import os

import click

import releasetool.secrets
import releasetool.update_check
import releasetool.commands.publish_reporter
import releasetool.commands.start.python
import releasetool.commands.start.python_tool
import releasetool.commands.start.nodejs
import releasetool.commands.start.java
import releasetool.commands.start.ruby
import releasetool.commands.start.go
import releasetool.commands.tag.python
import releasetool.commands.tag.python_tool
import releasetool.commands.tag.nodejs
import releasetool.commands.tag.java
import releasetool.commands.tag.ruby


class _OptionPromptIfNone(click.Option):
    """A custom option that only prompts if the default value can't be
    determined."""

    _value_key = "_default_val"

    def get_default(self, ctx):
        if not hasattr(self, self._value_key):
            default = super(_OptionPromptIfNone, self).get_default(ctx)
            setattr(self, self._value_key, default)
        return getattr(self, self._value_key)

    def prompt_for_value(self, ctx):
        default = self.get_default(ctx)

        # only prompt if the default value is None
        if default is None:
            return super(_OptionPromptIfNone, self).prompt_for_value(ctx)

        return default


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(message="%(version)s")
def main(ctx):
    if ctx.invoked_subcommand is None:
        return ctx.invoke(start)


def _detect_language():
    if os.path.exists("package.json"):
        return "nodejs"
    elif os.path.exists("setup.py"):
        if os.path.exists("google"):
            return "python"
        else:
            return "python-tool"
    elif os.path.exists("Gemfile"):
        return "ruby"
    elif os.path.exists("pom.xml") or os.path.exists("build.gradle"):
        return "java"
    return None


_language_choices = ["python", "python-tool", "nodejs", "java", "ruby", "go"]


def _language_option():
    return click.option(
        "--language",
        prompt=f"Which language ({', '.join(_language_choices)})?",
        type=click.Choice(_language_choices),
        default=_detect_language,
        cls=_OptionPromptIfNone,
    )


@main.command()
@_language_option()
def start(language):
    releasetool.update_check.check_for_updates(
        "gcp-releasetool", print=functools.partial(click.secho, fg="magenta")
    )

    if language == "python":
        return releasetool.commands.start.python.start()
    if language == "python-tool":
        return releasetool.commands.start.python_tool.start()
    if language == "nodejs":
        return releasetool.commands.start.nodejs.start()
    if language == "java":
        return releasetool.commands.start.java.start()
    if language == "ruby":
        return releasetool.commands.start.ruby.start()
    if language == "go":
        return releasetool.commands.start.go.start()


@main.command()
@_language_option()
def tag(language):
    if language == "python":
        return releasetool.commands.tag.python.tag()
    if language == "python-tool":
        return releasetool.commands.tag.python_tool.tag()
    if language == "nodejs":
        return releasetool.commands.tag.nodejs.tag()
    if language == "java":
        return releasetool.commands.tag.java.tag()
    if language == "ruby":
        return releasetool.commands.tag.ruby.tag()


@main.command(name="reset-config")
def reset_config():
    releasetool.secrets.delete_password()


@main.command(name="publish-reporter-start")
@click.option("--github_token", envvar="GITHUB_TOKEN", default=None)
@click.option("--pr", envvar="AUTORELEASE_PR", default=None)
def publish_reporter_start(github_token: str, pr: str):
    releasetool.commands.publish_reporter.start(github_token, pr)


@main.command(name="publish-reporter-finish")
@click.option("--github_token", envvar="GITHUB_TOKEN", default=None)
@click.option("--pr", envvar="AUTORELEASE_PR", default=None)
@click.option("--status", type=bool, default=True)
@click.option("--details", envvar="PUBLISH_DETAILS", default=None)
def publish_reporter_finish(github_token: str, pr: str, status: bool, details: str):
    releasetool.commands.publish_reporter.finish(github_token, pr, status, details)


@main.command(name="publish-reporter-script")
def publish_reporter_script():
    releasetool.commands.publish_reporter.script()


if __name__ == "__main__":
    main()
