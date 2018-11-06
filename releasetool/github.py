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
from typing import Sequence, Union

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

    def list_pull_requests(
        self, repository: str, state: str = None, merged: bool = True
    ) -> Sequence[dict]:
        url = f"{_GITHUB_ROOT}/repos/{repository}/pulls"
        response = self.session.get(url, params={"state": state})
        response.raise_for_status()

        if merged:
            return [pull for pull in response.json() if pull["merged_at"] is not None]

        return response.json()

    def get_pull_request(self, repository: str, number: str) -> dict:
        url = f"{_GITHUB_ROOT}/repos/{repository}/pulls/{number}"
        response = self.session.get(url)
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
        match = r"#(?P<pull_request>\d+)"
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

    def add_issue_labels(
        self, repository: str, issue_number: str, labels: Sequence[str]
    ) -> dict:
        url = f"{_GITHUB_ROOT}/repos/{repository}/issues/{issue_number}/labels"
        response = self.session.post(url, json={"labels": labels})
        response.raise_for_status()
        return response.json()

    def replace_issue_labels(
        self, owner: str, repository: str, number: str, labels: Sequence[str]
    ) -> dict:
        url = f"{_GITHUB_ROOT}/repos/{owner}/{repository}/issues/{number}/labels"
        response = self.session.put(url, json={"labels": labels})
        response.raise_for_status()
        return response.json()

    def update_pull_labels(
        self, pull: dict, add: Sequence[str] = None, remove: Sequence[str] = None
    ) -> dict:
        """Updates labels for a github pull, adding and removing labels as needed."""
        label_names = set([label["name"] for label in pull["labels"]])

        if add:
            label_names = label_names.union(add)

        if remove:
            label_names = label_names.difference(remove)

        return self.replace_issue_labels(
            owner=pull["base"]["repo"]["owner"]["login"],
            repository=pull["base"]["repo"]["name"],
            number=pull["number"],
            labels=list(label_names),
        )

    def create_pull_request_comment(
        self, repository: str, pull_request_number: Union[str, int], comment: str
    ) -> dict:
        repo_url = f"{_GITHUB_ROOT}/repos/{repository}"
        url = f"{repo_url}/issues/{pull_request_number}/comments"
        response = self.session.post(url, json={"body": comment})
        response.raise_for_status()
        return response.json()

    def get_release(self, repository: str, tag_name: str) -> dict:
        url = f"{_GITHUB_ROOT}/repos/{repository}/releases/tags/{tag_name}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_tag_sha(self, repository: str, tag_name: str) -> str:
        url = f"{_GITHUB_ROOT}/repos/{repository}/tags"
        response = self.session.get(url)
        response.raise_for_status()

        for tag in response.json():
            if tag["name"] == tag_name:
                return tag["commit"]["sha"]

        return None
