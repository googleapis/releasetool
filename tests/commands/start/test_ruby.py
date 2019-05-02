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

import pytest


@pytest.fixture
def mut():
    from releasetool.commands.start import ruby

    return ruby


def test_determine_last_release(mut):
    context = mut.Context()
    context.tags = ["google-cloud-spanner/v1.1.1", "google-cloud/v2.2.2"]
    context.package_name = "google-cloud"

    mut.determine_last_release(context)
    assert context.last_release_committish == "google-cloud/v2.2.2"
    assert context.last_release_version == "2.2.2"
