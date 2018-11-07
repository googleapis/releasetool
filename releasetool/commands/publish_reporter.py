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

"""Used by publish CI jobs to report status back to GitHub."""

import os
import pkgutil
import re
from typing import Tuple

import releasetool.github


def figure_out_github_token(github_token: str) -> str:
    # This script is designed to run in Kokoro. There's several sources where
    # the GitHub token could be, and we want to make adding this script easy.
    # We'll try the common ones before giving up.

    # A valid github token was passed on the command line, make sure it's
    # not a file and just return it.
    if github_token is not None:
        if os.path.exists(github_token):
            with open(github_token, "r", encoding="utf-8") as fh:
                return fh.read().strip()
        else:
            return github_token

    # First, try KeyStore
    paths = []
    if "KOKORO_KEYSTORE_DIR" in os.environ:
        paths.append(
            os.path.join(
                os.environ["KOKORO_KEYSTORE_DIR"], "73713_yoshi-automation-github-key"
            )
        )

    # Second, try gfile resources.
    if "KOKORO_GFILE_DIR" in os.environ:
        paths.append(os.path.join(os.environ["KOKORO_GFILE_DIR"], "github-token.txt"))

    for path in paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read().strip()

    return None


def extract_pr_details(pr) -> Tuple[str, str, str]:
    match = re.match(
        r"https://github\.com/(?P<owner>.+?)/(?P<repo>.+?)/pull/(?P<number>\d+?)$", pr
    )

    if not match:
        raise ValueError("Not a PR URL.")

    return match.group("owner"), match.group("repo"), match.group("number")


def start(github_token: str, pr: str) -> None:
    """Reports the start of a publication job to GitHub."""
    github_token = figure_out_github_token(github_token)

    if not github_token or not pr:
        print("No github token or PR specified to report status to, returning.")
        return

    gh = releasetool.github.GitHub(github_token)

    try:
        owner, repo, number = extract_pr_details(pr)
    except ValueError:
        print("Invalid PR number, returning.")
        return

    build_url = os.environ.get("CLOUD_LOGGING_URL")

    if not build_url:
        kokoro_build_id = os.environ.get("KOKORO_BUILD_ID")

        if kokoro_build_id:
            build_url = f"http://sponge/{kokoro_build_id}"

    if build_url:
        message = f"The release build has started, the log can be viewed [here]({build_url}). :sunflower:"
    else:
        message = f"The release build has started, but the build log URL could not be determined. :broken_heart:"

    gh.create_pull_request_comment(f"{owner}/{repo}", number, message)


def finish(github_token: str, pr: str, status: bool, details: str) -> None:
    """Reports the completion of a publication job to GitHub."""
    github_token = figure_out_github_token(github_token)

    if not github_token or not pr:
        print("No github token or PR specified to report status to, returning.")
        return

    gh = releasetool.github.GitHub(github_token)

    try:
        owner, repo, number = extract_pr_details(pr)
    except ValueError:
        print("Invalid PR number, returning.")
        return

    if status:
        message = ":egg: You hatched a release! The release build finished successfully! :purple_heart:"
        labels = ["autorelease: published"]
    else:
        message = "The release build failed! Please investigate!"
        labels = ["autorelease: failed"]

    if details:
        message += f"\n{details}"

    gh.create_pull_request_comment(f"{owner}/{repo}", number, message)

    pull = gh.get_pull_request(f"{owner}/{repo}", number)

    gh.update_pull_labels(pull, add=labels, remove=["autorelease: tagged"])


def script():
    resource = pkgutil.get_data("releasetool.commands", "publish_reporter.sh")
    print(resource.decode("utf-8"), flush=True)
