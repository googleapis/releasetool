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

from releasetool.commands.tag.nodejs import _get_latest_release_notes
from releasetool.commands.common import TagContext

fixture_old_style_changelog = """
# Changelog

[npm history][1]

[1]: https://www.npmjs.com/package/dialogflow?activeTab=versions

## v0.8.2

03-13-2019 16:30 PDT

### Bug Fixes
- fix: throw on invalid credentials ([#281](https://github.com/googleapis/nodejs-dialogflow/pull/281))

## v0.8.1

01-28-2019 13:24 PST

### Documentation
- fix(docs): dialogflow inn't published under @google-cloud scope ([#266](https://github.com/googleapis/nodejs-dialogflow/pull/266))

## v0.8.0
"""

fixture_new_and_old_style_changelog = """
# Changelog

[npm history][1]

[1]: https://www.npmjs.com/package/@google-cloud/os-login?activeTab=versions

### [0.3.3](https://www.github.com/googleapis/nodejs-os-login/compare/v0.3.2...v0.3.3) (2019-04-30)


### Bug Fixes

* include 'x-goog-request-params' header in requests ([#167](https://www.github.com/googleapis/nodejs-os-login/issues/167)) ([074051d](https://www.github.com/googleapis/nodejs-os-login/commit/074051d))

## v0.3.2

03-18-2019 13:47 PDT

### Implementation Changes
- refactor: update json import paths ([#156](https://github.com/googleapis/nodejs-os-login/pull/156))
- fix: throw on invalid credentials
"""

fixture_new_style_changelog = """
# Change Log

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [2.0.0](https://www.github.com/bcoe/examples-conventional-commits/compare/v1.3.0...v2.0.0) (2019-04-29)


### Features

* added the most amazing feature ever ([42f90e2](https://www.github.com/bcoe/examples-conventional-commits/commit/42f90e2))
* adds a fancy new feature ([c46bfa3](https://www.github.com/bcoe/examples-conventional-commits/commit/c46bfa3))


### BREAKING CHANGES

* this fancy new feature breaks things
* disclaimer breaks everything

## [1.3.0](https://github.com/bcoe/examples-conventional-commits/compare/v1.2.1...v1.3.0) (2018-11-03)
"""


def test_old_style_release_notes():
    """
    Our old CHANGELOG template does not make the version header a link and
    always uses H2 headers.
    """
    expected = """03-13-2019 16:30 PDT

### Bug Fixes
- fix: throw on invalid credentials ([#281](https://github.com/googleapis/nodejs-dialogflow/pull/281))"""
    ctx = TagContext(release_version="v0.8.2")
    _get_latest_release_notes(ctx, fixture_old_style_changelog)
    assert ctx.release_notes == expected


def test_new_style_release_notes_patch():
    """
    In the conventional-commits template (see: https://github.com/conventional-changelog/conventional-changelog),
    patches are an H3 header and are linked to the underlying issue that created the release.
    """
    expected = """### Bug Fixes

* include 'x-goog-request-params' header in requests ([#167](https://www.github.com/googleapis/nodejs-os-login/issues/167)) ([074051d](https://www.github.com/googleapis/nodejs-os-login/commit/074051d))"""
    ctx = TagContext(release_version="v0.3.3")
    _get_latest_release_notes(ctx, fixture_new_and_old_style_changelog)
    assert ctx.release_notes == expected


def test_new_style_release_notes_breaking():
    """
    in the conventional-commits template, features/breaking-changes use an H2 header.
    """
    expected = """### Features

* added the most amazing feature ever ([42f90e2](https://www.github.com/bcoe/examples-conventional-commits/commit/42f90e2))
* adds a fancy new feature ([c46bfa3](https://www.github.com/bcoe/examples-conventional-commits/commit/c46bfa3))


### BREAKING CHANGES

* this fancy new feature breaks things
* disclaimer breaks everything"""
    ctx = TagContext(release_version="v2.0.0")
    _get_latest_release_notes(ctx, fixture_new_style_changelog)
    assert ctx.release_notes == expected
