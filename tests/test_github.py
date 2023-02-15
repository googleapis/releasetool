# Copyright 2023 Google LLC
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
from releasetool import github
import pathlib
import requests_mock


def test_app_credentials():
    with requests_mock.Mocker() as m:
        m.post(
            "https://api.github.com/app/installations/my-installation-id/access_tokens",
            status_code=201,
            json={
                "token": "remote-access-token",
            },
        )

        private_key = (
            pathlib.Path(__file__).parent / "testdata" / "fake-private-key.pem"
        ).read_text()
        token = github.get_installation_access_token(
            "my-app-id", "my-installation-id", private_key
        )
        assert token == "remote-access-token"
