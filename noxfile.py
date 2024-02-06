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

import nox
import pathlib

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

ALL_PYTHON = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]

@nox.session(python='3.8')
def blacken(session):
    session.install('black')
    session.run('black', 'autorelease', 'releasetool', 'tests')


@nox.session(python='3.8')
def lint(session):
    session.install('mypy==0.812', 'flake8', 'black')
    session.run('pip', 'install', '-e', '.')
    session.run('black', '--check', 'autorelease', 'releasetool', 'tests')
    session.run('flake8', 'autorelease', 'releasetool', 'tests')
    session.run(
        'mypy',
        '--no-strict-optional',
        '--ignore-missing-imports',
        'releasetool')


@nox.session(python=ALL_PYTHON)
def test(session):
    session.install('pytest')
    # Use a constraints file for the specific python runtime version.
    # We do this to make sure that we're testing against the lowest
    # supported version of a dependency.
    constraints_file = f"{CURRENT_DIRECTORY}/testing/constraints-{session.python}.txt"
    session.run('pip', 'install', '-e', '.', "-r", constraints_file)
    session.run('pip', 'install', 'requests_mock')
    session.run('pytest', 'tests', *session.posargs)
