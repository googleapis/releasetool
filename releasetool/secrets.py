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
import keyring

_SERVICE = "com.google.cloud.devrel.releasetool"


def get_password(name):
    return keyring.get_password(_SERVICE, name)


def set_password(name, password):
    """Ensure we have a github username and token."""
    keyring.set_password(_SERVICE, "github", password)


def delete_password():
    keyring.delete_password(_SERVICE, "github")


def ensure_password(name, prompt):
    password = get_password(name)

    if not password:
        password = click.prompt(prompt)
        set_password(name, password)

    return password
