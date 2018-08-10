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

import os
import re
import tempfile
from typing import Optional

import click


def open_editor(filename: str, return_contents: bool = False) -> Optional[str]:
    click.edit(filename=filename)

    if return_contents:
        with open(filename, "r") as fh:
            return fh.read()
    else:
        return None


def open_editor_with_content(
    filename: str, contents: str, return_contents: bool = False
) -> Optional[str]:

    with open(filename, "w") as fh:
        fh.write(contents)

    return open_editor(filename, return_contents=return_contents)


def open_editor_with_tempfile(contents: str, suffix: str = ".txt") -> Optional[str]:
    handle, filename = tempfile.mkstemp(suffix)
    os.close(handle)

    content = open_editor_with_content(filename, contents, return_contents=True)

    os.remove(filename)

    return content


def insert_before(
    filename: str, new_content: str, expr: str, separator: str = "\n"
) -> None:
    with open(filename, "r+") as fh:
        if not new_content.endswith(separator):
            new_content += separator

        content = fh.read()
        match = re.search(expr, content, re.MULTILINE)

        if not match:
            return

        position = match.start()

        output = content[:position] + new_content + content[position:]

        fh.seek(0)
        fh.write(output)


def replace(filename: str, expr: str, replacement: str) -> None:
    with open(filename, "r+") as fh:
        content = fh.read()

        content = re.sub(expr, replacement, content)

        fh.seek(0)
        fh.write(content)
        fh.truncate()
