# Copyright 2019 Google LLC
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

from unittest import mock

import pytest


@pytest.fixture
def mut():
    from releasetool.commands.start import python

    return python


@pytest.mark.parametrize(
    "setup_py_contents,release_version,expected",
    [
        ("version = '1.0.0'\n", "1.1.0", "version = '1.1.0'\n"),
        ('version = "1.0.0"\n', "1.1.0", 'version = "1.1.0"\n'),
    ],
)
def test_update_setup_py_sets_version(
    mut, setup_py_contents, release_version, expected
):
    context = mut.Context()
    context.release_version = release_version

    with mock.patch(
        "builtins.open", mock.mock_open(read_data=setup_py_contents)
    ) as mock_open:
        mut.update_setup_py(context)
        mock_file = mock_open()
        mock_file.write.assert_called_once_with(expected)
