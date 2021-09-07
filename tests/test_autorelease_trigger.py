# Copyright 2021 Google LLC
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

from unittest.mock import patch, Mock

from autorelease import trigger


@patch("autorelease.trigger.trigger_kokoro_build_for_pull_request")
@patch("autorelease.github.GitHub.list_org_issues")
@patch("autorelease.kokoro.make_authorized_session")
def test_no_issues(
    make_authorized_session, list_org_issues, trigger_kokoro_build_for_pull_request
):
    list_org_issues.return_value = []

    trigger.main("github-token", "kokoro-credentials")
    make_authorized_session.assert_called_once()
    trigger_kokoro_build_for_pull_request.assert_not_called()


@patch("autorelease.trigger.trigger_kokoro_build_for_pull_request")
@patch("autorelease.github.GitHub.list_org_issues")
@patch("autorelease.kokoro.make_adc_session")
def test_adc(make_adc_session, list_org_issues, trigger_kokoro_build_for_pull_request):
    list_org_issues.return_value = []

    trigger.main("github-token", None)
    make_adc_session.assert_called_once()
    trigger_kokoro_build_for_pull_request.assert_not_called()


@patch("autorelease.trigger.trigger_kokoro_build_for_pull_request")
@patch("autorelease.github.GitHub.list_org_issues")
@patch("autorelease.kokoro.make_authorized_session")
def test_processes_issues(
    make_authorized_session, list_org_issues, trigger_kokoro_build_for_pull_request
):
    pr1 = {
        "base": {"ref": "abc123", "repo": {"full_name": "googleapis/java-asset"}},
        "pull_request": {"html_url": "https://github.com/googleapis/java-asset"},
        "title": "chore: release 1.2.3",
    }
    pr2 = {
        "base": {"ref": "def456", "repo": {"full_name": "googleapis/nodejs-container"}},
        "pull_request": {"html_url": "https://github.com/nodejs/java-container"},
        "title": "chore: release 1.0.0",
    }
    list_org_issues.side_effect = [[pr1, pr2]]
    trigger.main("github-token", "kokoro-credentials")
    list_org_issues.assert_any_call(
        org="googleapis",
        state="closed",
        labels="autorelease: tagged",
        created_after="2021-04-01",
    )
    list_org_issues.assert_any_call(
        org="GoogleCloudPlatform",
        state="closed",
        labels="autorelease: tagged",
        created_after="2021-04-01",
    )
    assert trigger_kokoro_build_for_pull_request.call_count == 2


@patch("autorelease.kokoro.trigger_build")
def test_trigger_kokoro_build_for_pull_request_skips_non_merged(trigger_build):
    github = Mock()
    github.update_pull_labels = Mock()
    github.get_url.return_value = {
        "merged_at": None,
        "base": {"repo": {"full_name": "googleapis/java-asset"}},
    }
    issue = {
        "pull_request": {"url": "https://api.github.com/googleapis/java-asset/pull/5"}
    }
    trigger.trigger_kokoro_build_for_pull_request(Mock(), github, issue, Mock())
    github.update_pull_labels.assert_called_once()
    trigger_build.assert_not_called()


@patch("autorelease.trigger.LANGUAGE_ALLOWLIST", ["java"])
@patch("autorelease.kokoro.trigger_build")
def test_trigger_kokoro_build_for_pull_request_triggers_kokoro(trigger_build):
    github = Mock()
    github.get_url.return_value = {
        "merged_at": "2021-01-01T09:00:00.000Z",
        "merge_commit_sha": "abcd1234",
        "base": {"repo": {"full_name": "googleapis/java-asset"}},
        "html_url": "https://github.com/googleapis/java-asset/pulls/5",
    }
    issue = {
        "pull_request": {"url": "https://api.github.com/googleapis/java-asset/pull/5"},
        "merged_at": "2021-01-01T09:00:00.000Z",
    }

    trigger.trigger_kokoro_build_for_pull_request(Mock(), github, issue, Mock())
    trigger_build.assert_called_once()
    github.update_pull_labels.assert_called_once()


@patch("autorelease.trigger.LANGUAGE_ALLOWLIST", [])
@patch("autorelease.kokoro.trigger_build")
def test_trigger_kokoro_build_for_pull_request_skips_kokoro_if_not_in_allowlist(
    trigger_build,
):
    github = Mock()
    github.get_url.return_value = {
        "merged_at": "2021-01-01T09:00:00.000Z",
        "merge_commit_sha": "abcd1234",
        "base": {"repo": {"full_name": "googleapis/java-asset"}},
        "html_url": "https://github.com/googleapis/java-asset/pulls/5",
    }
    issue = {
        "pull_request": {"url": "https://api.github.com/googleapis/java-asset/pull/5"},
        "merged_at": "2021-01-01T09:00:00.000Z",
    }
    trigger.trigger_kokoro_build_for_pull_request(Mock(), github, issue, Mock())
    trigger_build.assert_not_called()


@patch("autorelease.trigger.LANGUAGE_ALLOWLIST", ["php"])
@patch("autorelease.kokoro.trigger_build")
def test_trigger_kokoro_build_for_pull_request_skips_kokoro_if_no_job_name(
    trigger_build,
):
    github = Mock()
    github.get_url.return_value = {
        "merged_at": "2021-01-01T09:00:00.000Z",
        "base": {"repo": {"full_name": "googleapis/google-cloud-php"}},
        "html_url": "https://github.com/googleapis/google-cloud-php/pulls/5",
    }
    issue = {
        "pull_request": {
            "url": "https://api.github.com/googleapis/google-cloud-php/pull/5"
        },
        "merged_at": "2021-01-01T09:00:00.000Z",
    }
    trigger.trigger_kokoro_build_for_pull_request(Mock(), github, issue, Mock())
    trigger_build.assert_not_called()


@patch("autorelease.trigger.LANGUAGE_ALLOWLIST", ["php"])
@patch("autorelease.kokoro.trigger_build")
def test_trigger_kokoro_build_for_pull_request_skips_kokoro_if_already_triggered(
    trigger_build,
):
    github = Mock()
    github.get_url.return_value = {
        "merged_at": "2021-01-01T09:00:00.000Z",
        "base": {"repo": {"full_name": "googleapis/google-cloud-php"}},
        "html_url": "https://github.com/googleapis/google-cloud-php/pulls/5",
        "labels": [{"id": 12345, "name": "autorelease: triggered"}],
    }
    issue = {
        "pull_request": {
            "url": "https://api.github.com/googleapis/google-cloud-php/pull/5"
        },
        "merged_at": "2021-01-01T09:00:00.000Z",
    }
    trigger.trigger_kokoro_build_for_pull_request(Mock(), github, issue, Mock())
    trigger_build.assert_not_called()


@patch("autorelease.trigger.LANGUAGE_ALLOWLIST", ["java"])
@patch("autorelease.kokoro.make_authorized_session")
@patch("autorelease.github.GitHub.get_issue")
@patch("autorelease.github.GitHub.get_url")
@patch("autorelease.github.GitHub.update_pull_labels")
@patch("autorelease.kokoro.trigger_build")
def test_trigger_single(
    trigger_build, update_pull_labels, get_url, get_issue, make_authorized_session
):
    kokoro_session = Mock()
    make_authorized_session.return_value = kokoro_session
    get_issue.return_value = {
        "title": "chore: release 1.2.3",
        "pull_request": {
            "html_url": "https://github.com/googleapis/java-trace/pull/1234",
            "url": "https://api.github.com/repos/googleapis/java-trace/pulls/1234",
        },
    }
    get_url.return_value = {
        "merged_at": "2021-07-20T09:00:00.123Z",
        "base": {"repo": {"full_name": "googleapis/java-trace"}},
        "html_url": "https://github.com/googleapis/java-trace/pull/1234",
        "merge_commit_sha": "abcd1234",
        "labels": [{"id": 12345, "name": "autorelease: tagged"}],
    }

    pull_request_url = "https://github.com/googleapis/java-trace/pull/1234"
    reporter = trigger.trigger_single(
        "fake-github-token", "fake-kokoro-credentials", pull_request_url
    )

    assert len(reporter.results) == 1
    trigger_build.assert_called_with(
        kokoro_session,
        job_name="cloud-devrel/client-libraries/java/java-trace/release/stage",
        sha="abcd1234",
        env_vars={
            "AUTORELEASE_PR": "https://github.com/googleapis/java-trace/pull/1234"
        },
    )
    update_pull_labels.assert_not_called()


@patch("autorelease.kokoro.make_authorized_session")
@patch("autorelease.kokoro.trigger_build")
def test_trigger_single_bad_url(trigger_build, make_authorized_session):
    kokoro_session = Mock()
    make_authorized_session.return_value = kokoro_session

    pull_request_url = "https://github.com/googleapis/java-trace/issues/1234"
    reporter = trigger.trigger_single(
        "fake-github-token", "fake-kokoro-credentials", pull_request_url
    )

    assert len(reporter.results) == 1
    trigger_build.assert_not_called()


@patch("autorelease.kokoro.make_authorized_session")
@patch("autorelease.github.GitHub.get_issue")
@patch("autorelease.github.GitHub.get_url")
@patch("autorelease.github.GitHub.update_pull_labels")
@patch("autorelease.kokoro.trigger_build")
def test_trigger_single_skips_already_triggered(
    trigger_build, update_pull_labels, get_url, get_issue, make_authorized_session
):
    kokoro_session = Mock()
    make_authorized_session.return_value = kokoro_session
    get_issue.return_value = {
        "title": "chore: release 1.2.3",
        "pull_request": {
            "html_url": "https://github.com/googleapis/java-trace/pull/1234",
            "url": "https://api.github.com/repos/googleapis/java-trace/pulls/1234",
        },
    }
    get_url.return_value = {
        "merged_at": "2021-07-20T09:00:00.123Z",
        "base": {"repo": {"full_name": "googleapis/java-trace"}},
        "html_url": "https://github.com/googleapis/java-trace/pull/1234",
        "merge_commit_sha": "abcd1234",
        "labels": [
            {"id": 12345, "name": "autorelease: tagged"},
            {"id": 12346, "name": "autorelease: triggered"},
        ],
    }

    pull_request_url = "https://github.com/googleapis/java-trace/pull/1234"
    reporter = trigger.trigger_single(
        "fake-github-token", "fake-kokoro-credentials", pull_request_url
    )

    assert len(reporter.results) == 1
    trigger_build.assert_not_called()
