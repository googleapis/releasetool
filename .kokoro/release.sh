#!/bin/bash

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

set -eo pipefail

# Enable the publish build reporter
# Note: this installs from source since we're in the releasetool repo. Other projects
# will need to use python3 -m pip install gcp-releasetool
python3 -m pip install github/releasetool --require-hashes -r github/releasetool/requirements.txt

python3 -m releasetool publish-reporter-script > /tmp/publisher-script; source /tmp/publisher-script

# Move into the package, build the distribution and upload.
cd github/releasetool
TWINE_PASSWORD=$(cat "${KOKORO_KEYSTORE_DIR}/73713_google-cloud-pypi-token-keystore-1")

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

python3 setup.py sdist bdist_wheel
python3 -m twine upload --username __token__ --password "${TWINE_PASSWORD}" dist/*
