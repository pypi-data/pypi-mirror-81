# wp-dataops-pyutil
This provides **`wpdatautil`**, a Python 3.8 package with specific reusable utility functions for data processing.

A limited version of this readme which is published to PyPI is [available separately](README_PyPI.md).

[![cicd badge](https://github.com/wqpredtech/wp-dataops-pyutil/workflows/cicd/badge.svg?branch=master)](https://github.com/wqpredtech/wp-dataops-pyutil/actions?query=workflow%3Acicd+branch%3Amaster)

| [GitHub Releases/Changelog](https://github.com/wqpredtech/wp-dataops-pyutil/releases) | [PyPI release](https://pypi.org/project/wpdatautil/) |
|-|-|

## Usage
`pip install -U wpdatautil` will install the package and all loosely-versioned [requirements](requirements/install.txt).
The implemented utilities are broadly organized by their primary third-party or builtin package requirement.

## Development
### Setup
To set up the project locally:
1. Install Python 3.8
1. Clone the repo and setup a corresponding new IDE project.
1. Use the IDE to create a virtual environment for this repo and project.
1. Configure the IDE to use a max line length of 180. This is also defined in various static analyzer configuration files in the project.
It facilitates the use of descriptive variable names while ensuring that lines still display fully.
1. Run `./scripts/install_requirements.sh` to install the loosely-versioned requirements.
1. Run `./scripts/test.sh` and ensure an exitcode of 0 to confirm that all configured static analysis checks and unit tests pass.
### Publish
To publish the package to PyPI:
1. Ensure the commits which are to be released are merged into `master`, and the build is passing.
1. Ensure the intended new semver, e.g. "0.1.2" is defined in `version` in [`setup.py`](setup.py) in `master`, and the build is passing.
1. Create and publish a [new release on GitHub](https://github.com/wqpredtech/wp-dataops-pyutil/releases/new) with the semver tag, e.g. "v0.1.2", and a changelog since the last release.
This triggers the deployment [workflow](https://github.com/wqpredtech/wp-dataops-pyutil/actions?query=workflow%3Acicd) which publishes the release to PyPI.
1. Confirm that the published version is [listed on PyPI](https://pypi.org/project/wpdatautil/#history).
### Contribute
To contribute to this repository, create a pull request into `master` with sufficient unit test coverage for the changes.
