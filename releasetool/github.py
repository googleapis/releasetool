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

import base64
import re
from typing import Sequence

import requests


_GITHUB_ROOT: str = "https://api.github.com"
_GITHUB_UI_ROOT: str = "https://github.com"


class GitHub:
    def __init__(self, token: str) -> None:
        self.session: requests.Session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {token}",
            }
        )

    def list_pull_requests(self, repository: str, state: str = None) -> Sequence[dict]:
        url = f"{_GITHUB_ROOT}/repos/{repository}/pulls"
        response = self.session.get(url, params={"state": state})
        response.raise_for_status()
        return response.json()

    def create_pull_request(
        self, repository: str, head: str, title: str, body: str = None
    ) -> dict:
        url = f"{_GITHUB_ROOT}/repos/{repository}/pulls"
        response = self.session.post(
            url,
            json={
                "title": title,
                "body": body,
                "head": head,
                "base": "master",
                "maintainer_can_modify": True,
            },
        )
        response.raise_for_status()
        return response.json()

    def link_pull_request(self, text: str, repository: str) -> str:
        match = "#(?P<pull_request>\d+)"
        url = f"{_GITHUB_UI_ROOT}/{repository}/pull/\\g<pull_request>"
        replacement = f"[#\\g<pull_request>]({url})"
        return re.sub(match, replacement, text)

    def get_contents(self, repository: str, path: str, ref: str = None) -> bytes:
        url = f"{_GITHUB_ROOT}/repos/{repository}/contents/{path}"
        response = self.session.get(url, params={"ref": ref})
        response.raise_for_status()
        return base64.b64decode(response.json()["content"])

    def create_release(
        self,
        repository: str,
        tag_name: str,
        target_committish: str,
        name: str,
        body: str,
    ) -> dict:
        url = f"{_GITHUB_ROOT}/repos/{repository}/releases"
        response = self.session.post(
            url,
            json={
                "tag_name": tag_name,
                "target_committish": target_committish,
                "name": name,
                "body": body,
            },
        )
        response.raise_for_status()
        return response.json()

    def create_pull_request_comment(
        self, repository: str, pull_request_number: int, comment: str
    ) -> dict:
        repo_url = f"{_GITHUB_ROOT}/repos/{repository}"
        url = f"{repo_url}/issues/{pull_request_number}/comments"
        response = self.session.post(url, json={"body": comment})
        response.raise_for_status()
        return response.json()
