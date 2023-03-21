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

import argparse
import os
import sys

from autorelease import tag, trigger

# TODO(busunkim): Fetch magictoken from KMS once KMS setup is complete.
_KEYSTORE_GITHUB_TOKEN_LOCATION = "73713_yoshi-automation-github-key"


def _determine_github_token(github_token):
    """Automatically use the GitHub token provided by Keystore if needed."""
    if github_token is not None:
        return github_token

    if "KOKORO_KEYSTORE_DIR" in os.environ:
        filename = os.path.join(
            os.environ["KOKORO_KEYSTORE_DIR"], _KEYSTORE_GITHUB_TOKEN_LOCATION
        )

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as fh:
                return fh.read().strip()

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report")
    parser.add_argument("--github-token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument(
        "--kokoro-credentials", default=os.environ.get("AUTORELEASE_KOKORO_CREDENTIALS")
    )
    parser.add_argument("--pull", default=None)
    parser.add_argument("command")
    parser.add_argument("--multi-scm", action="store_true")

    args = parser.parse_args()

    args.github_token = _determine_github_token(args.github_token)

    if args.command == "tag":
        report = tag.main(args.github_token, args.kokoro_credentials)

        if args.report:
            report.write(args.report)

        if report.failures:
            sys.exit(2)
        else:
            return
    elif args.command == "trigger":
        report = trigger.main(args.github_token, args.kokoro_credentials)

        if args.report:
            report.write(args.report)

        if report.failures:
            sys.exit(2)
        else:
            return
    elif args.command == "trigger-single":
        if not args.pull:
            raise Exception("missing required arg --pull")
        report = trigger.trigger_single(
            args.github_token,
            args.kokoro_credentials,
            args.pull,
            multi_scm=args.multi_scm,
        )

        if args.report:
            report.write(args.report)

        if report.failures:
            sys.exit(2)
        else:
            return
    else:
        print(f"Unknown command {args.command}.")
        sys.exit(1)


if __name__ == "__main__":
    main()
