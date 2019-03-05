# Releasetool (for client libraries)

This tool helps create releases for cloud client libraries.

Presently, this works for Python, Node.js, and Ruby.  However, it's designed
in such a way that it could easily be used for other languages.


## Installation

**Requirements:**
- Python 3.6 or Python 3.7
- pip

We recommend following [this guide](https://docs.python-guide.org/starting/installation/#installation-guides) for installing both Python 3 and pip. 

Install releasetool using pip:
```
python3 -m pip install --user --upgrade gcp-releasetool
```

## Usage

Packages are published in two phases. First, a PR is created to update
`CHANGELOG.md` and the version number. Second, once the PR is merged the
merge commit is tagged and CI publishes the package.

To start the process of releasing use `releasetool start` from the directory of
the client you want to publish, for example:

```
git clone git@github.com:GoogleCloudPlatform/google-cloud-python.git
cd google-cloud-python
cd bigquery
releasetool start
```
This will create a PR.

**If the PR has a `autorelease: pending` label:**

Upon approval and merging,
`autorelease` will pick up the PR and run `releasetool tag` and release the
package to their respective package managers. Autorelease will comment on the release PR with the status of the release. [Example PR](https://github.com/googleapis/nodejs-pubsub/pull/521)

**Otherwise:**

Once the PR has been approved and merged, you can run `releasetool tag` from
anywhere in the repository to tag the commit and start CI.

```
git fetch origin master
git checkout origin/master
releasetool tag
```

### Resetting the GitHub Token

If you need to change the GitHub API token associated with releasetool, run `releasetool reset-config`. This will delete the existing token. The next time you run `releasetool start` you will be
prompted to enter a new token.
