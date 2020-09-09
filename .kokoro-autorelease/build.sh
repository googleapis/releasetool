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

cd ${KOKORO_ARTIFACTS_DIR}/git/autorelease

# Upgrade the NPM version
sudo npm install -g npm

# Kokoro currently uses 3.6.1
pyenv global 3.6.1

# Disable buffering, so that the logs stream through.
export PYTHONUNBUFFERED=1

# Add github to known hosts.
ssh-keyscan github.com >> ~/.ssh/known_hosts

# The key for triggering Kokoro jobs is a Keystore resource, so it'll be here.
export AUTORELEASE_KOKORO_CREDENTIALS=${KOKORO_KEYSTORE_DIR}/73713_kokoro_trigger_credentials

python3 -m pip install --quiet --user --upgrade -r requirements.txt
python3 -m autorelease --report sponge_log.xml ${AUTORELEASE_COMMAND}
