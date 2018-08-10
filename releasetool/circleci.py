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

from typing import Iterator, Optional
import time
from datetime import datetime

import requests

_CIRCLE_ROOT: str = "https://circleci.com/api/v1.1"


class CircleCI:
    def __init__(self, repository: str, vcs: str = "github") -> None:
        self.session: requests.Session = requests.Session()
        self.vcs = vcs
        self.repo = repository

    def get_latest_build_by_tag(self, tag: str, retries: int = 15) -> Optional[dict]:
        url = f"{_CIRCLE_ROOT}/project/{self.vcs}/{self.repo}"

        for retry in range(1, retries):
            response = self.session.get(url)
            response.raise_for_status()
            for build in response.json():
                if "branch" in build.keys() and build["vcs_tag"] == tag:
                    return build
            time.sleep(retry)

        return None

    def get_latest_build_by_branch(self, branch_name: str) -> Optional[dict]:
        url = f"{_CIRCLE_ROOT}/project/{self.vcs}/{self.repo}"

        response = self.session.get(url)
        response.raise_for_status()
        for build in response.json():
            if "branch" in build.keys() and build["branch"] == branch_name:
                return build

        return None

    def get_fresh_build_by_branch(
        self, branch_name: str, seconds_fresh: int = 60, retries: int = 15
    ) -> Optional[dict]:
        """
        Find a build that is less than seconds_fresh old. Useful if you
        need to find a build that isn't an old run
        """
        for retry in range(1, retries):
            build = self.get_latest_build_by_branch(branch_name)
            if not build:
                continue
            build_queued = build["queued_at"]
            queued_time = datetime.strptime(build_queued, "%Y-%m-%dT%H:%M:%S.%fZ")
            time_delta = datetime.utcnow() - queued_time
            if time_delta.total_seconds() <= seconds_fresh:
                return build

            # we either didn't find a build (hasn't been queued) or we
            # found a build but it was stale. Wait for new build to be queued.
            time.sleep(retry)
        return None

    def get_build(self, build_num: str) -> dict:
        url = f"{_CIRCLE_ROOT}/project/{self.vcs}/{self.repo}/{build_num}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_link_to_build(self, build_num: int):
        # API vcs and FE vcs are different
        vcs_map = {"github": "gh"}
        if self.vcs in vcs_map.keys():
            url_vcs = vcs_map[self.vcs]
        else:
            # if we don't have it in the mapping provide it directly.
            url_vcs = self.vcs

        # https://circleci.com/gh/GitHubUser/RepositoryName/1234
        return f"https://circleci.com/{url_vcs}/{self.repo}/{build_num}"

    def get_build_status_generator(self, build_num: str) -> Iterator[str]:
        """
        Returns a generator that polls circle for the status of a branch. It
        continues to return results until it enters a finished state
        """
        """
        lifecycle_states = [
            "queued", "scheduled", "not_run", "not_running", "running",
            "finished" ]

        build_status_states = [
            "retried", "canceled", "infrastructure_fail", "timedout",
            "not_run", "running", "failed", "queued", "scheduled",
            "not_running", "no_tests", "fixed", "success" ]
        """
        build = self.get_build(build_num)
        while "lifecycle" in build.keys() and build["lifecycle"] != "finished":
            yield build["status"]
            time.sleep(10)
            build = self.get_build(build_num)
        yield build["status"]
        return
