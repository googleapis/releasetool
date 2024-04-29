# Copyright 2021 Google LLC
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

from releasetool.commands.tag.php import kokoro_job_name, package_name


def test_kokoro_job_name():
    job_name = kokoro_job_name("upstream-owner/upstream-repo", "some-package-name")
    assert (
        job_name
        == "cloud-devrel/client-libraries/php/upstream-owner/upstream-repo/release"
    )
    job_name = kokoro_job_name("upstream-owner/google-cloud-php", "some-package-name")
    assert job_name == "cloud-devrel/client-libraries/php/google-cloud-php/docs/docs"


def test_package_name():
    name = package_name({"head": {"ref": "release-storage-v1.2.3"}})
    assert name is None
