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

"""This module talks to Kokoro via Pub/Sub messages to devrel-prod.googleplex.com."""

import base64

from google.auth.transport import requests
from google.oauth2 import service_account
import google.auth

from protos import kokoro_api_pb2


_DEVREL_PROD_KOKORO_TOPIC = (
    "projects/google.com:devrel-library-tracker-prod/topics/kokoro"
)


def _send_pubsub_message(
    session: requests.AuthorizedSession, topic: str, data: str
) -> dict:
    url = f"https://pubsub.googleapis.com/v1/{topic}:publish"
    encoded_data = base64.b64encode(data.encode("utf-8"))

    publish_request = {"messages": [{"data": encoded_data.decode("utf-8")}]}

    resp = session.post(url, json=publish_request)
    resp.raise_for_status()

    return resp


def _make_build_request(
    job_name: str, sha: str, env_vars: dict = None, multi_scm: bool = False
) -> str:
    request = kokoro_api_pb2.BuildRequest(
        full_job_name=job_name,
    )
    if multi_scm:
        request.scm_revision.github_scm_revision.commit_sha = sha
    else:
        request.multi_scm_revision.github_scm_revision.add(commit_sha=sha)

    if env_vars:
        for key, value in env_vars.items():
            request.env_vars[key] = value

    # Transform into a string for TextFormat. See:
    # https://sites.google.com/a/google.com/protocol-buffers/user-docs/miscellaneous-howtos/text-format-examples
    return str(request)


def make_authorized_session(credentials_file: str) -> requests.AuthorizedSession:
    """Create a scoped, authorized requests session using a service account

    Args:
        credentials_file {str}: Path to service account file

    Returns:
        requests.AuthorizedSession: The authorized requests session
    """
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=["https://www.googleapis.com/auth/pubsub"]
    )
    session = requests.AuthorizedSession(credentials)
    return session


def make_adc_session() -> requests.AuthorizedSession:
    """Create a scoped, authorized requests session using ADC

    Returns:
        requests.AuthorizedSession: The authorized requests session

    Raises:
        DefaultCredentialsError if no credentials found
    """
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/pubsub"]
    )
    session = requests.AuthorizedSession(credentials)
    return session


def trigger_build(
    session: requests.AuthorizedSession,
    job_name: str,
    sha: str,
    env_vars: dict = None,
    multi_scm: bool = False,
):
    build_request = _make_build_request(
        job_name, sha, env_vars=env_vars, multi_scm=multi_scm
    )
    _send_pubsub_message(session, _DEVREL_PROD_KOKORO_TOPIC, build_request)
