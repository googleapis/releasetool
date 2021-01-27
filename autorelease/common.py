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

import json
import re

from typing import Dict, Any, Callable
from autorelease.github import GitHub


def _determine_language(
    fetch_repos_json: Callable[[], str], repo_full_name: str
) -> str:
    python_tools = ["synthtool"]

    if repo_full_name.split("/")[1] in python_tools:
        return "python_tool"

    repos = json.loads(fetch_repos_json())["repos"]
    for repo in repos:
        if repo_full_name == repo["repo"]:
            return repo["language"]

    raise Exception("Unable to determine repository language.")


def determine_language(gh: GitHub, pull: Dict[str, Any]) -> str:
    name = pull["base"]["repo"]["full_name"]

    def fetch_repos_json():
        return gh.get_contents("googleapis/sloth", "repos.json")

    return _determine_language(fetch_repos_json, name)


"""Language names as reported by github."""
_SILVER_LANGUAGE_NAMES = {
    "JavaScript": "nodejs",
    "TypeScript": "nodejs",
    "Python": "python",
    "Java": "java",
    "PHP": "php",
    "Ruby": "ruby",
    "Go": "go",
    "C#": "dotnet",
    "Elixir": "elixer",
}


def guess_language(gh: GitHub, repo_full_name: str) -> str:
    special_cases = {
        # 2 special cases inherited from the original determine_language() code.
        "googleapis/synthtool": "python_tool",
        # 2 more special cases where the most prevalent language is not the same as
        # what was declared in the old repos.json.
        "GoogleCloudPlatform/cloud-code-samples": "dotnet",
        "googleapis/doc-templates": "python",
    }
    special_case = special_cases.get(repo_full_name)
    if special_case:
        return special_case

    # Does the repo name have a language name in it?
    lang_names = {
        "cpp",
        "dotnet",
        "elixir",
        "go",
        "java",
        "nodejs",
        "php",
        "python",
        "python_tool",
        "ruby",
    }
    chunks = set(re.split("/|-", repo_full_name))
    x = lang_names.intersection(chunks)
    if 1 == len(x):
        return x.pop()  # Found the language name in the repo name

    # Fetch how many lines of each language are found in the repo.
    languages = gh.get_languages(repo_full_name)
    ranks = [
        (count, lang)
        for (lang, count) in languages.items()
        # Ignore languages we don't care about, like Shell.
        if lang in _SILVER_LANGUAGE_NAMES
    ]
    ranks.sort(reverse=True)
    if ranks:
        # Return the most prevalent language in the repo.
        return _SILVER_LANGUAGE_NAMES[ranks[0][1]]
    else:
        raise Exception("Unable to determine repository language.")
