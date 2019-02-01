import requests


MAGIC_PROXY_ENDPOINT = "http://magic-github-proxy.endpoints.devrel-dev.cloud.goog"

scopes = [
    "POST /repos/googleapis/.+/issues/.+/comments",  # add comments to issues
    "GET /repos/googleapis/.+/pulls/.+",  # get pull requests
    "PUT /repos/googleapis/.+/issues/.+/labels",  # add labels to pull requests
]

response = requests.post(
    f"{MAGIC_PROXY_ENDPOINT}/magictoken",
    json={"github_token": GITHUB_TOKEN, "scopes": scopes},
    params={"key": MAGIC_PROXY_API_KEY},
)
response.raise_for_status()
token = response.text
print(token)


# test access releases w/ invalid token

session = requests.Session()
session.proxies = {"http:": MAGIC_PROXY_ENDPOINT, "https": MAGIC_PROXY_ENDPOINT}
session.headers["Authorization"] = f"Bearer {token}"
session.params["key"] = MAGIC_PROXY_API_KEY

session.get("http://api.github.com/googleapis/releasetool/releases")
