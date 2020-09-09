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

import json
import os
import pathlib
import string

from autorelease import github
from autorelease.common import _determine_language, guess_language


def repo_name_to_test_name(repo_name: str) -> str:
    letters = []
    for letter in repo_name:
        if letter in string.ascii_lowercase:
            letters.append(letter)
        elif letter in string.ascii_uppercase:
            if letters:
                letters.append("_")
            letters.append(letter.lower())
        else:
            letters.append("_")
    return "test_guess_" + "".join(letters)


def test_determine_language():
    # determine_language() is the old function that depends on sloth's repo.json.
    # Use it to generate the code for test_guess_language() so we can confirm
    # the output is 100% the same.
    repos_json = (pathlib.Path(__file__).parent / "testdata" / "repos.json").read_text()
    repos = json.loads(repos_json)["repos"]

    python_tools_repo_names = [
        "googleapis/releasetool",
        "googleapis/synthtool",
        "googleapis/docuploader",
    ]

    repo_names = python_tools_repo_names + [repo["repo"] for repo in repos]
    languages = set()
    for name in repo_names:
        language = _determine_language(lambda: repos_json, name)
        languages.add((language, name))
    for language, name in sorted(languages):
        test_name = repo_name_to_test_name(name)
        print(
            f"""def {test_name}():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert {repr(language)} == guess_language(gh, {repr(name)})

"""
        )


def test_guess_google_cloud_platform_cpp_docs_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "cpp" == guess_language(gh, "GoogleCloudPlatform/cpp-docs-samples")


def test_guess_googleapis_google_cloud_cpp():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "cpp" == guess_language(gh, "googleapis/google-cloud-cpp")


def test_guess_google_cloud_platform_cloud_code_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "dotnet" == guess_language(gh, "GoogleCloudPlatform/cloud-code-samples")


def test_guess_google_cloud_platform_dotnet_docs_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "dotnet" == guess_language(gh, "GoogleCloudPlatform/dotnet-docs-samples")


def test_guess_google_cloud_platform_getting_started_dotnet():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "dotnet" == guess_language(gh, "GoogleCloudPlatform/getting-started-dotnet")


def test_guess_google_cloud_platform_stackdriver_sandbox():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "dotnet" == guess_language(gh, "GoogleCloudPlatform/stackdriver-sandbox")


def test_guess_googleapis_gapic_generator_csharp():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "dotnet" == guess_language(gh, "googleapis/gapic-generator-csharp")


def test_guess_googleapis_gax_dotnet():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "dotnet" == guess_language(gh, "googleapis/gax-dotnet")


def test_guess_googleapis_google_api_dotnet_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "dotnet" == guess_language(gh, "googleapis/google-api-dotnet-client")


def test_guess_googleapis_google_cloud_dotnet():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "dotnet" == guess_language(gh, "googleapis/google-cloud-dotnet")


def test_guess_google_cloud_platform_elixir_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "elixir" == guess_language(gh, "GoogleCloudPlatform/elixir-samples")


def test_guess_googleapis_elixir_google_api():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "elixir" == guess_language(gh, "googleapis/elixir-google-api")


def test_guess_google_cloud_platform_golang_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "go" == guess_language(gh, "GoogleCloudPlatform/golang-samples")


def test_guess_googleapis_gapic_generator_go():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "go" == guess_language(gh, "googleapis/gapic-generator-go")


def test_guess_googleapis_gax_go():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "go" == guess_language(gh, "googleapis/gax-go")


def test_guess_googleapis_go_genproto():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "go" == guess_language(gh, "googleapis/go-genproto")


def test_guess_googleapis_google_api_go_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "go" == guess_language(gh, "googleapis/google-api-go-client")


def test_guess_googleapis_google_cloud_go():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "go" == guess_language(gh, "googleapis/google-cloud-go")


def test_guess_googleapis_google_cloud_go_testing():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "go" == guess_language(gh, "googleapis/google-cloud-go-testing")


def test_guess_google_cloud_platform_getting_started_java():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "GoogleCloudPlatform/getting-started-java")


def test_guess_google_cloud_platform_java_docs_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "GoogleCloudPlatform/java-docs-samples")


def test_guess_googleapis_api_common_java():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/api-common-java")


def test_guess_googleapis_gapic_generator():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/gapic-generator")


def test_guess_googleapis_gax_java():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/gax-java")


def test_guess_googleapis_google_api_java_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/google-api-java-client")


def test_guess_googleapis_google_api_java_client_services():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/google-api-java-client-services")


def test_guess_googleapis_google_auth_library_java():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/google-auth-library-java")


def test_guess_googleapis_google_cloud_java():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/google-cloud-java")


def test_guess_googleapis_google_http_java_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/google-http-java-client")


def test_guess_googleapis_google_oauth_java_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/google-oauth-java-client")


def test_guess_googleapis_java_accessapproval():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-accessapproval")


def test_guess_googleapis_java_accesscontextmanager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-accesscontextmanager")


def test_guess_googleapis_java_analytics_admin():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-analytics-admin")


def test_guess_googleapis_java_asset():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-asset")


def test_guess_googleapis_java_automl():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-automl")


def test_guess_googleapis_java_bigquery():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-bigquery")


def test_guess_googleapis_java_bigqueryconnection():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-bigqueryconnection")


def test_guess_googleapis_java_bigquerydatatransfer():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-bigquerydatatransfer")


def test_guess_googleapis_java_bigqueryreservation():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-bigqueryreservation")


def test_guess_googleapis_java_bigquerystorage():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-bigquerystorage")


def test_guess_googleapis_java_bigtable():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-bigtable")


def test_guess_googleapis_java_bigtable_emulator():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-bigtable-emulator")


def test_guess_googleapis_java_bigtable_hbase():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-bigtable-hbase")


def test_guess_googleapis_java_billing():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-billing")


def test_guess_googleapis_java_billingbudgets():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-billingbudgets")


def test_guess_googleapis_java_cloud_bom():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-cloud-bom")


def test_guess_googleapis_java_cloudbuild():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-cloudbuild")


def test_guess_googleapis_java_common_protos():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-common-protos")


def test_guess_googleapis_java_compute():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-compute")


def test_guess_googleapis_java_conformance_tests():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-conformance-tests")


def test_guess_googleapis_java_container():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-container")


def test_guess_googleapis_java_containeranalysis():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-containeranalysis")


def test_guess_googleapis_java_core():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-core")


def test_guess_googleapis_java_datacatalog():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-datacatalog")


def test_guess_googleapis_java_datalabeling():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-datalabeling")


def test_guess_googleapis_java_dataproc():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-dataproc")


def test_guess_googleapis_java_datastore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-datastore")


def test_guess_googleapis_java_dialogflow():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-dialogflow")


def test_guess_googleapis_java_dlp():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-dlp")


def test_guess_googleapis_java_dns():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-dns")


def test_guess_googleapis_java_document_ai():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-document-ai")


def test_guess_googleapis_java_errorreporting():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-errorreporting")


def test_guess_googleapis_java_firestore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-firestore")


def test_guess_googleapis_java_functions():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-functions")


def test_guess_googleapis_java_game_servers():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-game-servers")


def test_guess_googleapis_java_gcloud_maven_plugin():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-gcloud-maven-plugin")


def test_guess_googleapis_java_grafeas():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-grafeas")


def test_guess_googleapis_java_iam():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-iam")


def test_guess_googleapis_java_iamcredentials():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-iamcredentials")


def test_guess_googleapis_java_iot():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-iot")


def test_guess_googleapis_java_irm():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-irm")


def test_guess_googleapis_java_kms():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-kms")


def test_guess_googleapis_java_language():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-language")


def test_guess_googleapis_java_logging():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-logging")


def test_guess_googleapis_java_logging_logback():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-logging-logback")


def test_guess_googleapis_java_mediatranslation():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-mediatranslation")


def test_guess_googleapis_java_memcache():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-memcache")


def test_guess_googleapis_java_monitoring():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-monitoring")


def test_guess_googleapis_java_monitoring_dashboards():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-monitoring-dashboards")


def test_guess_googleapis_java_notebooks():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-notebooks")


def test_guess_googleapis_java_notification():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-notification")


def test_guess_googleapis_java_orgpolicy():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-orgpolicy")


def test_guess_googleapis_java_os_config():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-os-config")


def test_guess_googleapis_java_os_login():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-os-login")


def test_guess_googleapis_java_phishingprotection():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-phishingprotection")


def test_guess_googleapis_java_pubsub():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-pubsub")


def test_guess_googleapis_java_pubsublite():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-pubsublite")


def test_guess_googleapis_java_recaptchaenterprise():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-recaptchaenterprise")


def test_guess_googleapis_java_recommendations_ai():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-recommendations-ai")


def test_guess_googleapis_java_recommender():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-recommender")


def test_guess_googleapis_java_redis():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-redis")


def test_guess_googleapis_java_resourcemanager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-resourcemanager")


def test_guess_googleapis_java_scheduler():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-scheduler")


def test_guess_googleapis_java_secretmanager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-secretmanager")


def test_guess_googleapis_java_securitycenter():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-securitycenter")


def test_guess_googleapis_java_securitycenter_settings():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-securitycenter-settings")


def test_guess_googleapis_java_servicedirectory():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-servicedirectory")


def test_guess_googleapis_java_shared_config():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-shared-config")


def test_guess_googleapis_java_shared_dependencies():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-shared-dependencies")


def test_guess_googleapis_java_spanner():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-spanner")


def test_guess_googleapis_java_spanner_jdbc():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-spanner-jdbc")


def test_guess_googleapis_java_speech():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-speech")


def test_guess_googleapis_java_storage():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-storage")


def test_guess_googleapis_java_storage_nio():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-storage-nio")


def test_guess_googleapis_java_talent():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-talent")


def test_guess_googleapis_java_tasks():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-tasks")


def test_guess_googleapis_java_texttospeech():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-texttospeech")


def test_guess_googleapis_java_trace():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-trace")


def test_guess_googleapis_java_translate():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-translate")


def test_guess_googleapis_java_video_intelligence():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-video-intelligence")


def test_guess_googleapis_java_vision():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-vision")


def test_guess_googleapis_java_webrisk():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-webrisk")


def test_guess_googleapis_java_websecurityscanner():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "java" == guess_language(gh, "googleapis/java-websecurityscanner")


def test_guess_google_cloud_platform_nodejs_docs_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "GoogleCloudPlatform/nodejs-docs-samples")


def test_guess_google_cloud_platform_nodejs_getting_started():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "GoogleCloudPlatform/nodejs-getting-started")


def test_guess_googleapis_cloud_debug_nodejs():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/cloud-debug-nodejs")


def test_guess_googleapis_cloud_profiler_nodejs():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/cloud-profiler-nodejs")


def test_guess_googleapis_cloud_trace_nodejs():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/cloud-trace-nodejs")


def test_guess_googleapis_code_suggester():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/code-suggester")


def test_guess_googleapis_gapic_generator_typescript():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/gapic-generator-typescript")


def test_guess_googleapis_gax_nodejs():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/gax-nodejs")


def test_guess_googleapis_gaxios():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/gaxios")


def test_guess_googleapis_gcp_metadata():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/gcp-metadata")


def test_guess_googleapis_gcs_resumable_upload():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/gcs-resumable-upload")


def test_guess_googleapis_github_repo_automation():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/github-repo-automation")


def test_guess_googleapis_google_api_nodejs_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/google-api-nodejs-client")


def test_guess_googleapis_google_auth_library_nodejs():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/google-auth-library-nodejs")


def test_guess_googleapis_google_cloud_node():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/google-cloud-node")


def test_guess_googleapis_google_p___pem():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/google-p12-pem")


def test_guess_googleapis_jsdoc_fresh():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/jsdoc-fresh")


def test_guess_googleapis_jsdoc_region_tag():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/jsdoc-region-tag")


def test_guess_googleapis_node_gtoken():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/node-gtoken")


def test_guess_googleapis_nodejs_analytics_admin():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-analytics-admin")


def test_guess_googleapis_nodejs_asset():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-asset")


def test_guess_googleapis_nodejs_automl():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-automl")


def test_guess_googleapis_nodejs_bigquery():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-bigquery")


def test_guess_googleapis_nodejs_bigquery_connection():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-bigquery-connection")


def test_guess_googleapis_nodejs_bigquery_data_transfer():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-bigquery-data-transfer")


def test_guess_googleapis_nodejs_bigquery_reservation():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-bigquery-reservation")


def test_guess_googleapis_nodejs_bigquery_storage():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-bigquery-storage")


def test_guess_googleapis_nodejs_bigtable():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-bigtable")


def test_guess_googleapis_nodejs_billing():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-billing")


def test_guess_googleapis_nodejs_billing_budgets():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-billing-budgets")


def test_guess_googleapis_nodejs_cloud_container():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-cloud-container")


def test_guess_googleapis_nodejs_cloudbuild():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-cloudbuild")


def test_guess_googleapis_nodejs_common():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-common")


def test_guess_googleapis_nodejs_compute():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-compute")


def test_guess_googleapis_nodejs_containeranalysis():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-containeranalysis")


def test_guess_googleapis_nodejs_datacatalog():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-datacatalog")


def test_guess_googleapis_nodejs_datalabeling():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-datalabeling")


def test_guess_googleapis_nodejs_dataproc():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-dataproc")


def test_guess_googleapis_nodejs_datastore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-datastore")


def test_guess_googleapis_nodejs_datastore_kvstore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-datastore-kvstore")


def test_guess_googleapis_nodejs_datastore_session():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-datastore-session")


def test_guess_googleapis_nodejs_dialogflow():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-dialogflow")


def test_guess_googleapis_nodejs_dlp():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-dlp")


def test_guess_googleapis_nodejs_dns():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-dns")


def test_guess_googleapis_nodejs_document_ai():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-document-ai")


def test_guess_googleapis_nodejs_error_reporting():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-error-reporting")


def test_guess_googleapis_nodejs_firestore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-firestore")


def test_guess_googleapis_nodejs_firestore_session():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-firestore-session")


def test_guess_googleapis_nodejs_functions():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-functions")


def test_guess_googleapis_nodejs_game_servers():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-game-servers")


def test_guess_googleapis_nodejs_gce_images():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-gce-images")


def test_guess_googleapis_nodejs_googleapis_common():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-googleapis-common")


def test_guess_googleapis_nodejs_grafeas():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-grafeas")


def test_guess_googleapis_nodejs_iot():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-iot")


def test_guess_googleapis_nodejs_irm():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-irm")


def test_guess_googleapis_nodejs_kms():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-kms")


def test_guess_googleapis_nodejs_language():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-language")


def test_guess_googleapis_nodejs_local_auth():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-local-auth")


def test_guess_googleapis_nodejs_logging():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-logging")


def test_guess_googleapis_nodejs_logging_bunyan():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-logging-bunyan")


def test_guess_googleapis_nodejs_logging_winston():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-logging-winston")


def test_guess_googleapis_nodejs_media_translation():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-media-translation")


def test_guess_googleapis_nodejs_memcache():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-memcache")


def test_guess_googleapis_nodejs_monitoring():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-monitoring")


def test_guess_googleapis_nodejs_monitoring_dashboards():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-monitoring-dashboards")


def test_guess_googleapis_nodejs_os_config():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-os-config")


def test_guess_googleapis_nodejs_os_login():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-os-login")


def test_guess_googleapis_nodejs_paginator():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-paginator")


def test_guess_googleapis_nodejs_phishing_protection():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-phishing-protection")


def test_guess_googleapis_nodejs_precise_date():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-precise-date")


def test_guess_googleapis_nodejs_projectify():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-projectify")


def test_guess_googleapis_nodejs_promisify():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-promisify")


def test_guess_googleapis_nodejs_proto_files():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-proto-files")


def test_guess_googleapis_nodejs_pubsub():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-pubsub")


def test_guess_googleapis_nodejs_rcloadenv():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-rcloadenv")


def test_guess_googleapis_nodejs_recaptcha_enterprise():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-recaptcha-enterprise")


def test_guess_googleapis_nodejs_recommender():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-recommender")


def test_guess_googleapis_nodejs_redis():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-redis")


def test_guess_googleapis_nodejs_resource():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-resource")


def test_guess_googleapis_nodejs_scheduler():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-scheduler")


def test_guess_googleapis_nodejs_secret_manager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-secret-manager")


def test_guess_googleapis_nodejs_security_center():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-security-center")


def test_guess_googleapis_nodejs_service_directory():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-service-directory")


def test_guess_googleapis_nodejs_spanner():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-spanner")


def test_guess_googleapis_nodejs_speech():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-speech")


def test_guess_googleapis_nodejs_storage():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-storage")


def test_guess_googleapis_nodejs_talent():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-talent")


def test_guess_googleapis_nodejs_tasks():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-tasks")


def test_guess_googleapis_nodejs_text_to_speech():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-text-to-speech")


def test_guess_googleapis_nodejs_translate():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-translate")


def test_guess_googleapis_nodejs_video_intelligence():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-video-intelligence")


def test_guess_googleapis_nodejs_vision():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-vision")


def test_guess_googleapis_nodejs_web_risk():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/nodejs-web-risk")


def test_guess_googleapis_release_please():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/release-please")


def test_guess_googleapis_repo_automation_bots():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/repo-automation-bots")


def test_guess_googleapis_sloth():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/sloth")


def test_guess_googleapis_teeny_request():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "nodejs" == guess_language(gh, "googleapis/teeny-request")


def test_guess_google_cloud_platform_getting_started_php():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "GoogleCloudPlatform/getting-started-php")


def test_guess_google_cloud_platform_php_docs_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "GoogleCloudPlatform/php-docs-samples")


def test_guess_googleapis_gax_php():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/gax-php")


def test_guess_googleapis_google_api_php_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-api-php-client")


def test_guess_googleapis_google_api_php_client_services():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-api-php-client-services")


def test_guess_googleapis_google_auth_library_php():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-auth-library-php")


def test_guess_googleapis_google_cloud_php():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php")


def test_guess_googleapis_google_cloud_php_asset():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-asset")


def test_guess_googleapis_google_cloud_php_automl():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-automl")


def test_guess_googleapis_google_cloud_php_bigquery():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-bigquery")


def test_guess_googleapis_google_cloud_php_bigquerydatatransfer():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(
        gh, "googleapis/google-cloud-php-bigquerydatatransfer"
    )


def test_guess_googleapis_google_cloud_php_bigtable():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-bigtable")


def test_guess_googleapis_google_cloud_php_common_protos():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-common-protos")


def test_guess_googleapis_google_cloud_php_container():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-container")


def test_guess_googleapis_google_cloud_php_core():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-core")


def test_guess_googleapis_google_cloud_php_dataproc():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-dataproc")


def test_guess_googleapis_google_cloud_php_datastore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-datastore")


def test_guess_googleapis_google_cloud_php_debugger():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-debugger")


def test_guess_googleapis_google_cloud_php_dialogflow():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-dialogflow")


def test_guess_googleapis_google_cloud_php_dlp():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-dlp")


def test_guess_googleapis_google_cloud_php_errorreporting():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-errorreporting")


def test_guess_googleapis_google_cloud_php_firestore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-firestore")


def test_guess_googleapis_google_cloud_php_iot():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-iot")


def test_guess_googleapis_google_cloud_php_irm():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-irm")


def test_guess_googleapis_google_cloud_php_kms():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-kms")


def test_guess_googleapis_google_cloud_php_language():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-language")


def test_guess_googleapis_google_cloud_php_logging():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-logging")


def test_guess_googleapis_google_cloud_php_monitoring():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-monitoring")


def test_guess_googleapis_google_cloud_php_oslogin():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-oslogin")


def test_guess_googleapis_google_cloud_php_pubsub():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-pubsub")


def test_guess_googleapis_google_cloud_php_recommender():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-recommender")


def test_guess_googleapis_google_cloud_php_redis():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-redis")


def test_guess_googleapis_google_cloud_php_scheduler():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-scheduler")


def test_guess_googleapis_google_cloud_php_secret_manager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-secret-manager")


def test_guess_googleapis_google_cloud_php_security_center():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-security-center")


def test_guess_googleapis_google_cloud_php_spanner():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-spanner")


def test_guess_googleapis_google_cloud_php_speech():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-speech")


def test_guess_googleapis_google_cloud_php_storage():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-storage")


def test_guess_googleapis_google_cloud_php_talent():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-talent")


def test_guess_googleapis_google_cloud_php_tasks():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-tasks")


def test_guess_googleapis_google_cloud_php_text_to_speech():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-text-to-speech")


def test_guess_googleapis_google_cloud_php_trace():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-trace")


def test_guess_googleapis_google_cloud_php_translate():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-translate")


def test_guess_googleapis_google_cloud_php_videointelligence():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-videointelligence")


def test_guess_googleapis_google_cloud_php_vision():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-vision")


def test_guess_googleapis_google_cloud_php_web_risk():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(gh, "googleapis/google-cloud-php-web-risk")


def test_guess_googleapis_google_cloud_php_web_security_scanner():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "php" == guess_language(
        gh, "googleapis/google-cloud-php-web-security-scanner"
    )


def test_guess_google_cloud_platform_getting_started_python():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "GoogleCloudPlatform/getting-started-python")


def test_guess_google_cloud_platform_python_docs_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "GoogleCloudPlatform/python-docs-samples")


def test_guess_googleapis_dialogflow_python_client_v_():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/dialogflow-python-client-v2")


def test_guess_googleapis_doc_pipeline():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/doc-pipeline")


def test_guess_googleapis_doc_templates():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/doc-templates")


def test_guess_googleapis_gapic_generator_python():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/gapic-generator-python")


def test_guess_googleapis_google_api_python_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/google-api-python-client")


def test_guess_googleapis_google_auth_library_python():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/google-auth-library-python")


def test_guess_googleapis_google_auth_library_python_oauthlib():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(
        gh, "googleapis/google-auth-library-python-oauthlib"
    )


def test_guess_googleapis_google_cloud_python():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/google-cloud-python")


def test_guess_googleapis_google_cloud_python_happybase():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/google-cloud-python-happybase")


def test_guess_googleapis_google_resumable_media_python():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/google-resumable-media-python")


def test_guess_googleapis_proto_plus_python():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/proto-plus-python")


def test_guess_googleapis_python_access_approval():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-access-approval")


def test_guess_googleapis_python_access_context_manager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-access-context-manager")


def test_guess_googleapis_python_analytics_admin():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-analytics-admin")


def test_guess_googleapis_python_api_common_protos():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-api-common-protos")


def test_guess_googleapis_python_api_core():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-api-core")


def test_guess_googleapis_python_asset():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-asset")


def test_guess_googleapis_python_audit_log():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-audit-log")


def test_guess_googleapis_python_automl():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-automl")


def test_guess_googleapis_python_bigquery():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-bigquery")


def test_guess_googleapis_python_bigquery_connection():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-bigquery-connection")


def test_guess_googleapis_python_bigquery_datatransfer():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-bigquery-datatransfer")


def test_guess_googleapis_python_bigquery_reservation():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-bigquery-reservation")


def test_guess_googleapis_python_bigquery_storage():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-bigquery-storage")


def test_guess_googleapis_python_bigtable():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-bigtable")


def test_guess_googleapis_python_billing():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-billing")


def test_guess_googleapis_python_billingbudgets():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-billingbudgets")


def test_guess_googleapis_python_cloud_core():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-cloud-core")


def test_guess_googleapis_python_cloudbuild():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-cloudbuild")


def test_guess_googleapis_python_container():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-container")


def test_guess_googleapis_python_containeranalysis():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-containeranalysis")


def test_guess_googleapis_python_crc__c():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-crc32c")


def test_guess_googleapis_python_datacatalog():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-datacatalog")


def test_guess_googleapis_python_datalabeling():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-datalabeling")


def test_guess_googleapis_python_dataproc():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-dataproc")


def test_guess_googleapis_python_datastore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-datastore")


def test_guess_googleapis_python_dlp():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-dlp")


def test_guess_googleapis_python_dns():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-dns")


def test_guess_googleapis_python_documentai():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-documentai")


def test_guess_googleapis_python_error_reporting():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-error-reporting")


def test_guess_googleapis_python_firestore():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-firestore")


def test_guess_googleapis_python_functions():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-functions")


def test_guess_googleapis_python_game_servers():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-game-servers")


def test_guess_googleapis_python_grafeas():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-grafeas")


def test_guess_googleapis_python_iam():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-iam")


def test_guess_googleapis_python_iot():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-iot")


def test_guess_googleapis_python_kms():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-kms")


def test_guess_googleapis_python_language():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-language")


def test_guess_googleapis_python_logging():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-logging")


def test_guess_googleapis_python_media_translation():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-media-translation")


def test_guess_googleapis_python_memcache():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-memcache")


def test_guess_googleapis_python_monitoring():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-monitoring")


def test_guess_googleapis_python_monitoring_dashboards():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-monitoring-dashboards")


def test_guess_googleapis_python_ndb():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-ndb")


def test_guess_googleapis_python_notebooks():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-notebooks")


def test_guess_googleapis_python_org_policy():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-org-policy")


def test_guess_googleapis_python_os_config():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-os-config")


def test_guess_googleapis_python_oslogin():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-oslogin")


def test_guess_googleapis_python_phishingprotection():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-phishingprotection")


def test_guess_googleapis_python_pubsub():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-pubsub")


def test_guess_googleapis_python_recaptcha_enterprise():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-recaptcha-enterprise")


def test_guess_googleapis_python_recommendations_ai():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-recommendations-ai")


def test_guess_googleapis_python_recommender():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-recommender")


def test_guess_googleapis_python_redis():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-redis")


def test_guess_googleapis_python_resource_manager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-resource-manager")


def test_guess_googleapis_python_runtimeconfig():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-runtimeconfig")


def test_guess_googleapis_python_scheduler():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-scheduler")


def test_guess_googleapis_python_secret_manager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-secret-manager")


def test_guess_googleapis_python_securitycenter():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-securitycenter")


def test_guess_googleapis_python_service_directory():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-service-directory")


def test_guess_googleapis_python_spanner():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-spanner")


def test_guess_googleapis_python_spanner_django():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-spanner-django")


def test_guess_googleapis_python_speech():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-speech")


def test_guess_googleapis_python_storage():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-storage")


def test_guess_googleapis_python_talent():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-talent")


def test_guess_googleapis_python_tasks():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-tasks")


def test_guess_googleapis_python_test_utils():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-test-utils")


def test_guess_googleapis_python_texttospeech():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-texttospeech")


def test_guess_googleapis_python_trace():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-trace")


def test_guess_googleapis_python_translate():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-translate")


def test_guess_googleapis_python_videointelligence():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-videointelligence")


def test_guess_googleapis_python_vision():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-vision")


def test_guess_googleapis_python_webrisk():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-webrisk")


def test_guess_googleapis_python_websecurityscanner():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/python-websecurityscanner")


def test_guess_googleapis_sample_tester():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/sample-tester")


def test_guess_googleapis_docuploader():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python_tool" == guess_language(gh, "googleapis/docuploader")


def test_guess_googleapis_releasetool():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python" == guess_language(gh, "googleapis/releasetool")


def test_guess_googleapis_synthtool():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "python_tool" == guess_language(gh, "googleapis/synthtool")


def test_guess_google_cloud_platform_getting_started_ruby():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "GoogleCloudPlatform/getting-started-ruby")


def test_guess_google_cloud_platform_ruby_docs_samples():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "GoogleCloudPlatform/ruby-docs-samples")


def test_guess_googleapis_discovery_artifact_manager():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/discovery-artifact-manager")


def test_guess_googleapis_gapic_generator_ruby():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/gapic-generator-ruby")


def test_guess_googleapis_gax_ruby():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/gax-ruby")


def test_guess_googleapis_google_api_ruby_client():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/google-api-ruby-client")


def test_guess_googleapis_google_auth_library_ruby():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/google-auth-library-ruby")


def test_guess_googleapis_google_cloud_ruby():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/google-cloud-ruby")


def test_guess_googleapis_ruby_spanner_activerecord():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/ruby-spanner-activerecord")


def test_guess_googleapis_ruby_style():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/ruby-style")


def test_guess_googleapis_signet():
    gh = github.GitHub(os.environ["GITHUB_TOKEN"])
    assert "ruby" == guess_language(gh, "googleapis/signet")
