# Releasetool (for client libraries)

This tool helps create releases for cloud client libraries. 

Presently, this only works for Python but it's designed in such a way that it
could easily be used for other languages.


## Installation

This tool requires Python 3.6. Either install it from python.org or use
pyenv to get 3.6.

Install using pip:

```
python3 -m pip install --upgrade gcp-releasetool
```

## Usage

### Python

Python packages are published in two phases. First, a PR is created to update
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

Once the PR has been approved and merged, you can run `releasetool tag` from
anywhere in the repository to tag the commit and start CI.
