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

import re
import subprocess
from typing import Dict, Sequence


def list_tags() -> Sequence[str]:
    subprocess.check_output(["git", "fetch", "--tags"])
    output = subprocess.check_output(
        ["git", "tag", "--list", "--sort=-creatordate"]
    ).decode("utf-8")
    tags = output.split("\n")

    return tags


def get_latest_commit(branch: str) -> str:
    commit = subprocess.check_output(
        ["git", "log", "-1", branch, "--pretty=%H"]
    ).decode("utf-8")
    return commit


def summary_log(from_: str, to: str = "master", where: str = ".") -> Sequence[str]:
    output = subprocess.check_output(
        ["git", "log", "--format=%s", f"{from_}..{to}", where]
    ).decode("utf-8")
    commits = output.strip().split("\n")
    return commits


def checkout_create_branch(branch_name: str, base: str = "master") -> None:
    subprocess.check_output(["git", "checkout", "-b", branch_name, base])


def commit(files: Sequence[str], message: str) -> None:
    """Create a release commit."""
    subprocess.check_output(["git", "add"] + list(files))
    subprocess.check_output(["git", "commit", "-m", message])


def push(branch: str, remote: str = "origin") -> None:
    """Push the release branch to the remote."""
    subprocess.check_output(["git", "push", "-u", remote, branch])


def get_config() -> Dict[str, str]:
    output = subprocess.check_output(["git", "config", "--list"]).decode("utf-8")

    lines = [line for line in output.split("\n") if line]
    pairs = [line.split("=", 1) for line in lines]
    config = {key: value for key, value in pairs}

    return config


def get_remotes() -> Dict[str, str]:
    config = get_config()

    remote_names = []

    for key in config.keys():
        match = re.match(r"remote\.(?P<name>.+?)\.url", key)
        if match:
            remote_names.append(match.group("name"))

    remotes = {name: config[f"remote.{name}.url"] for name in remote_names}
    return remotes


def get_github_remotes() -> Dict[str, str]:
    """Returns a dictionary mapping remote names to the appropriate github
    owner/repo string."""
    remotes = get_remotes()

    github_repos = {}

    for name, url in remotes.items():
        # Match SSH or HTTP URLs, like:
        # git@github.com:GoogleCloudPlatform/google-cloud-python.git
        # https://github.com/GoogleCloudPlatform/google-cloud-python.git
        match = re.match(r"^git@github.com:(?P<name>.+)\.git$", url)
        if match:
            github_repos[name] = match.group("name")
            continue

        match = re.match(r"^https://(.+?)?github.com/(?P<name>.+)\.git$", url)
        if match:
            github_repos[name] = match.group("name")
            continue

    return github_repos
