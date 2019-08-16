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

from releasetool.commands.tag.java import _parse_release_notes, _parse_release_tag

RELEASETOOL_PR_DESCRIPTION = """
This pull request was generated using releasetool.

Some release notes here
"""

RELEASE_PLEASE_PR_DESCRIPTION = """
:robot: I have created a release \\*beep\\* \\*boop\\*
---
Some release notes here
---


This PR was generated with [Release Please](https://github.com/googleapis/release-please).
"""


def test_releasetool_release_notes():
    """
    Releasetool creates a PR with a specific lead in
    """
    expected = "Some release notes here"
    assert _parse_release_notes(RELEASETOOL_PR_DESCRIPTION) == expected


def test_release_please_release_notes():
    """
    release-please creates a PR with a specific lead in
    """
    expected = "Some release notes here"
    assert _parse_release_notes(RELEASE_PLEASE_PR_DESCRIPTION) == expected


def test_releasetool_release_tag():
    expected = "v1.2.3"
    assert _parse_release_tag("release-google-cloud-java-v1.2.3") == expected


def test_release_please_release_tag():
    expected = "v1.2.3"
    assert _parse_release_tag("release-v1.2.3") == expected
