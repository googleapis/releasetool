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


@pytest.mark.parametrize(
    "tags,package_name,expected",
    [
        (
            ["bonustag", "bigquery-1.3.0", "bigquery-1.2.0", "bigquery-1.0.0"],
            "bigquery",
            "bigquery-1.3.0",
        ),
        (
            [
                "bonustag",
                "bigquery-1.3.0",
                "bigquery-1.2.0",
                "bigquery_storage-0.2.0",
                "bigquery-1.0.0",
                "bigquery_datatransfer-0.3.0",
                "bigquery_datatransfer-0.2.0",
                "bigquery_storage-0.1.1",
                "bigquery_datatransfer-0.1.1",
                "bigquery_storage-0.1.0",
            ],
            "bigquery_storage",
            "bigquery_storage-0.2.0",
        ),
        (
            [
                "bonustag",
                "bigquery_datatransfer-0.3.0",
                "bigquery_storage-0.2.0",
                "bigquery-1.3.0",
                "bigquery-1.2.0",
                "bigquery-1.0.0",
                "bigquery_datatransfer-0.2.0",
                "bigquery_datatransfer-0.1.1",
                "bigquery_storage-0.1.1",
                "bigquery_storage-0.1.0",
            ],
            "bigquery",
            "bigquery-1.3.0",
        ),
        (
            [
                "mypackage-1.0.0",
                "bonustag",
                "mypackage-0.9.0",
            ],
            "myotherpackage",
            None,
        )
    ],
)
def find_last_release_tag(mut, tags, package_name, expected):
    candidate = mut.find_last_release_tag(tags, package_name)
    assert candidate == expected
