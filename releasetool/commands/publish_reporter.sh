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

if [ -f "${KOKORO_GFILE_DIR}/secret_manager/releasetool-publish-reporter-app" ]; then
    export APP_ID_PATH="${KOKORO_GFILE_DIR}/secret_manager/releasetool-publish-reporter-app"
    export INSTALLATION_ID_PATH="${KOKORO_GFILE_DIR}/secret_manager/releasetool-publish-reporter-googleapis-installation"
    export GITHUB_PRIVATE_KEY_PATH="${KOKORO_GFILE_DIR}/secret_manager/releasetool-publish-reporter-pem"
else
    echo 'could not load GitHub installation credentials'
fi

# Install an exit hook to report status.
releasetool_finish_report() {
    rv=$?
    if [[ $rv == 0 ]]; then
        python3 -m releasetool publish-reporter-finish --status yes || true
    else
        python3 -m releasetool publish-reporter-finish --status no || true
    fi
    echo "Release status reported."
    exit $rv
}

trap releasetool_finish_report EXIT

# Report the start of a build
python3 -m releasetool publish-reporter-start || true
