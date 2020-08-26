# Copyright 2020 Google LLC
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

import os
import pytest
import unittest
from unittest.mock import patch
import releasetool.commands.publish_reporter


class PublishReporter(unittest.TestCase):
    def test_publish_reporter_start_devrel_api_key(self):
        with patch.dict(os.environ, {"KOKORO_KEYSTORE_DIR": "./"}):
            with pytest.raises(Exception) as err:
                releasetool.commands.publish_reporter.start(
                    "abc123", "http://example.com"
                )
            assert "magic github proxy api key is required" in str(err.value)

    def test_publish_reporter_finish_devrel_api_key(self):
        with patch.dict(os.environ, {"KOKORO_KEYSTORE_DIR": "./"}):
            with pytest.raises(Exception) as err:
                releasetool.commands.publish_reporter.finish(
                    "abc123", "http://example.com", True, ""
                )
            assert "magic github proxy api key is required" in str(err.value)

    # TODO: use requests_mock to flesh out more thorough tests
    # see: https://github.com/googleapis/synthtool/blob/8cf6d2834ad14318e64429c3b94f6443ae83daf9/tests/test_language_java.py#L69-L76
