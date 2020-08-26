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
import json
import os
import re
import time

from typing import cast, List, Sequence, Union

import jwt
import requests
from cryptography.hazmat.backends import default_backend


_GITHUB_ROOT: str = "https://api.github.com"
_GITHUB_UI_ROOT: str = "https://github.com"
_MAGIC_GITHUB_PROXY_ROOT: str = (
    "https://magic-github-proxy.endpoints.devrel-prod.cloud.goog"
)


def _find_devrel_api_key() -> str:
    paths: List[str] = []
    magic_github_proxy_key: str = ""
    if "KOKORO_KEYSTORE_DIR" in os.environ:
        paths.append(
            os.path.join(
                os.environ["KOKORO_KEYSTORE_DIR"], "73713_magic-github-proxy-api-key"
            )
        )

    if "KOKORO_GFILE_DIR" in os.environ:
        paths.append(
            os.path.join(
                os.environ["KOKORO_GFILE_DIR"], "yoshi-magic-github-proxy-key.txt"
            )
        )

    for path in paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                magic_github_proxy_key = fh.read().strip()
                break

    if magic_github_proxy_key == "":
        raise Exception("A magic github proxy api key is required.")

    return magic_github_proxy_key


class GitHubToken:
    def __init__(self, token: Union[str, dict]):
        self.auth_type = 'Bearer'
        # If a dictionary is provided for token, assume it
        # contains app_id, installation, private_key, such that we
        # can fetch a JWT:
        if type(token) is dict:
            self.auth_type = "token"
            token_dict = cast(dict, token)
            self.token = self.application_access_token(
                token_dict["app_id"],
                token_dict["installation_id"],
                token_dict["private_key"],
            )

    def get_auth_type(self) -> str:
        return self.auth_type

    def get_token(self) -> str:
        return self.token

    def application_access_token(
        self, app_id: str, installation_id: str, private_key_str: str
    ) -> str:
        time_since_epoch_in_seconds = int(time.time())
        # see: https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-a-github-app
        payload = {
            "iat": time_since_epoch_in_seconds,
            "exp": time_since_epoch_in_seconds + (10 * 60),
            "iss": app_id,
        }

        private_key_bytes = private_key_str.encode()
        private_key = default_backend().load_pem_private_key(private_key_bytes, None)
        app_jwt = jwt.encode(payload, private_key, algorithm="RS256")

        headers = {
            "Authorization": "Bearer {}".format(app_jwt.decode()),
            "Accept": "application/vnd.github.machine-man-preview+json",
        }

        resp = requests.post(
            "https://api.github.com/installations/{}/access_tokens".format(
                installation_id
            ),
            headers=headers,
        )

        if resp.status_code != 201:
            raise Exception("Could exchange certificate for JWT.")
        return json.loads(resp.content.decode())["token"]


class GitHub:
    def __init__(self, token: GitHubToken, use_proxy: bool = False) -> None:
        self.session: requests.Session = requests.Session()
        self.GITHUB_ROOT = _GITHUB_ROOT
        self.session.headers.update(
            {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"{token.get_auth_type()} {token.get_token()}",
            }
        )

        if use_proxy:
            self.GITHUB_ROOT = _MAGIC_GITHUB_PROXY_ROOT
            # To use the proxy, we need an api key for the magic github proxy.
            self.session.params = {"key": _find_devrel_api_key()}

    def list_pull_requests(
        self, repository: str, state: str = None, merged: bool = True
    ) -> Sequence[dict]:
        url = f"{self.GITHUB_ROOT}/repos/{repository}/pulls"
        response = self.session.get(url, params={"state": state})
        response.raise_for_status()

        if merged:
            return [pull for pull in response.json() if pull["merged_at"] is not None]

        return response.json()

    def get_pull_request(self, repository: str, number: str) -> dict:
        url = f"{self.GITHUB_ROOT}/repos/{repository}/pulls/{number}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_pull_request(
        self,
        repository: str,
        head: str,
        title: str,
        body: str = None,
        base: str = "master",
    ) -> dict:
        url = f"{self.GITHUB_ROOT}/repos/{repository}/pulls"
        response = self.session.post(
            url,
            json={
                "title": title,
                "body": body,
                "head": head,
                "base": base,
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
        url = f"{self.GITHUB_ROOT}/repos/{repository}/contents/{path}"
        response = self.session.get(url, params={"ref": ref})
        response.raise_for_status()
        return base64.b64decode(response.json()["content"])

    def create_release(
        self,
        repository: str,
        tag_name: str,
        target_commitish: str,
        name: str,
        body: str,
        prerelease: bool = False,
    ) -> dict:
        url = f"{self.GITHUB_ROOT}/repos/{repository}/releases"
        response = self.session.post(
            url,
            json={
                "tag_name": tag_name,
                "target_commitish": target_commitish,
                "name": name,
                "body": body,
                "prerelease": prerelease,
            },
        )
        response.raise_for_status()
        return response.json()

    def add_issue_labels(
        self, repository: str, issue_number: str, labels: Sequence[str]
    ) -> dict:
        url = f"{self.GITHUB_ROOT}/repos/{repository}/issues/{issue_number}/labels"
        response = self.session.post(url, json={"labels": labels})
        response.raise_for_status()
        return response.json()

    def replace_issue_labels(
        self, owner: str, repository: str, number: str, labels: Sequence[str]
    ) -> dict:
        url = f"{self.GITHUB_ROOT}/repos/{owner}/{repository}/issues/{number}/labels"
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
        repo_url = f"{self.GITHUB_ROOT}/repos/{repository}"
        url = f"{repo_url}/issues/{pull_request_number}/comments"
        response = self.session.post(url, json={"body": comment})
        response.raise_for_status()
        return response.json()

    def get_release(self, repository: str, tag_name: str) -> dict:
        url = f"{self.GITHUB_ROOT}/repos/{repository}/releases/tags/{tag_name}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_tag_sha(self, repository: str, tag_name: str) -> str:
        url = f"{self.GITHUB_ROOT}/repos/{repository}/tags"
        response = self.session.get(url)
        response.raise_for_status()

        for tag in response.json():
            if tag["name"] == tag_name:
                return tag["commit"]["sha"]

        return None

    def delete_branch(self, repository: str, branch: str):
        url = f"{_GITHUB_ROOT}/repos/{repository}/git/refs/heads/{branch}"
        response = self.session.delete(url)
        response.raise_for_status()

        return None
