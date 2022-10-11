#!/usr/bin/env python3
"""Prompts the user and runs project setup during ``footing setup``"""
import os
import re
import subprocess
import sys

import requests


REPO_NAME = "{{ cookiecutter.repo_name }}"
MODULE_NAME = "{{ cookiecutter.module_name }}"
DESCRIPTION = "{{ cookiecutter.short_description }}"
FOOTING_ENV_VAR = "_FOOTING"
GITHUB_API_TOKEN_ENV_VAR = "GITHUB_API_TOKEN"
GITHUB_ORG_NAME = "Opus10"
GITHUB_REPO_API = f"/orgs/{GITHUB_ORG_NAME}/repos"
CIRCLECI_API_TOKEN_ENV_VAR = "CIRCLECI_API_TOKEN"


class Error(Exception):
    """Base exception for this script"""


class RemoteRepoExistsError(Error):
    """Thrown when a remote Github repo already exists"""


class GithubPushError(Error):
    """Thrown when there is an issue pushing to the remote repo"""


class CredentialsError(Error):
    """Thrown when the user does not have valid credentials to use template"""


def _shell(cmd, check=True, stdin=None, stdout=None, stderr=None):  # pragma: no cover
    """Runs a subprocess shell with check=True by default"""
    return subprocess.run(cmd, shell=True, check=check, stdin=stdin, stdout=stdout, stderr=stderr)


def get_user_input(prompt_text):
    return input(prompt_text).strip()


def yesno(message, default="yes", suffix=" "):
    """Prompt user to answer yes or no.

    Return True if the default is chosen, otherwise False.
    """
    if default == "yes":
        yesno_prompt = "[Y/n]"
    elif default == "no":
        yesno_prompt = "[y/N]"
    else:
        raise ValueError("default must be 'yes' or 'no'.")

    if message != "":
        prompt_text = f"{message} {yesno_prompt}{suffix}"
    else:
        prompt_text = f"{yesno_prompt}{suffix}"

    while True:
        response = get_user_input(prompt_text)
        if response == "":
            return True
        else:
            if re.match("^(y)(es)?$", response, re.IGNORECASE):
                if default == "yes":
                    return True
                else:
                    return False
            elif re.match("^(n)(o)?$", response, re.IGNORECASE):
                if default == "no":
                    return True
                else:
                    return False


class GithubClient:
    """Utility client for accessing Github API"""

    def __init__(self):
        self.api_token = os.environ[GITHUB_API_TOKEN_ENV_VAR]

    def _call_api(self, verb, url, check=True, **request_kwargs):
        """Perform a github API call

        Args:
            verb (str): Can be "post", "put", or "get"
            url (str): The base URL with a leading slash for Github API (v3)
        """
        api = "https://api.github.com{}".format(url)
        auth_headers = {"Authorization": "token {}".format(self.api_token)}
        headers = {**auth_headers, **request_kwargs.pop("headers", {})}
        resp = getattr(requests, verb)(api, headers=headers, **request_kwargs)
        if check:
            resp.raise_for_status()
        return resp

    def get(self, url, check=True, **request_kwargs):
        """Github API get"""
        return self._call_api("get", url, check=check, **request_kwargs)

    def post(self, url, check=True, **request_kwargs):
        """Github API post"""
        return self._call_api("post", url, check=check, **request_kwargs)

    def put(self, url, check=True, **request_kwargs):
        """Github API put"""
        return self._call_api("put", url, check=check, **request_kwargs)

    def patch(self, url, check=True, **request_kwargs):
        """Github API patch"""
        return self._call_api("patch", url, check=check, **request_kwargs)


def github_create_repo(
    repo_name,
    short_description,
    disable_squash_merge=True,
    disable_merge_commit=False,
    disable_rebase_merge=True,
    has_wiki=False,
    prompt=True,
):
    """Creates a remote github repo

    Args:
        repo_name (str): The github repository name
        short_description (str): A short description of the repository
        disable_squash_merge (bool, default=True): Disable squash merging of
            the repo
        disable_merge_commit (bool, default=False): Disable merge commit of
            the repo
        disable_rebase_merge (bool, default=True): Disable rebase merge of
            the repo
        has_wiki (bool, default=False): Disable wiki on repo.
        prompt (bool, default=True): Prompt the user to continue if any
            errors happen

    Raises:
        `RemoteRepoExistsError`: When the remote git repo already exists
    """
    github_client = GithubClient()
    resp = github_client.post(
        GITHUB_REPO_API,
        check=False,
        json={
            "name": repo_name,
            "description": short_description,
            "private": False,
            "has_wiki": has_wiki,
            "allow_squash_merge": not disable_squash_merge,
            "allow_merge_commit": not disable_merge_commit,
            "allow_rebase_merge": not disable_rebase_merge,
        },
    )

    repo_already_exists = resp.json().get("message") == "Repository creation failed."
    if resp.status_code == requests.codes.unprocessable and repo_already_exists:
        msg = (
            "Remote github repo already exists at"
            f" https://github.com/{GITHUB_ORG_NAME}/{repo_name}.git."
        )

        prompt_msg = (
            f"{msg} This can be from a previously failed setup run or"
            " because someone else already created the repository."
            " Continue without creating (y) or abort (n)?"
        )
        if prompt and yesno(prompt_msg, default="no"):
            raise RemoteRepoExistsError(msg)
    elif resp.status_code != requests.codes.created:
        print(
            f'An error happened during git repo creation - "{resp.json()}"',
            file=sys.stderr,
        )
        resp.raise_for_status()


def github_add_collaborators(repo_name, team_id, team_name, permission, prompt=True):
    """Adds Githbub collaborators for a repo

    Args:
        repo_name (str): The name of the Github repo
        team_id (int): The ID of the Github team
        team_name (str): The name of the Github team
        permission (str): The level of permission to grant the team
        prompt (bool, default=True): Prompt before adding permissions and
            skip if necessary
    """
    msg = (
        'Add {} access for the "{}" team on {} (if not, permissions will need'
        " to be configured later)?"
    ).format(permission, team_name, repo_name)
    if prompt and not yesno(msg, default="yes"):
        return False

    github_client = GithubClient()
    collaborators_api = f"/teams/{team_id}/repos/{GITHUB_ORG_NAME}/{repo_name}"
    github_client.put(collaborators_api, json={"permission": permission})

    return True


def github_setup_branch_protection(repo_name, branch, branch_protection):
    """Sets up branch protection for a repository

    Args:
        repo_name (str): The repository name
        branch (str): The branch to protect
        branch_protection (dict): A dictionary of parameters expected by
            the Github API. See
            developer.github.com/v3/repos/branches/#update-branch-protection
            for examples on the required input
    """
    github_client = GithubClient()
    protection_api = f"/repos/{GITHUB_ORG_NAME}/{repo_name}/branches/{branch}/protection"
    github_client.put(
        protection_api,
        json=branch_protection,
        headers={"Accept": "application/vnd.github.loki-preview+json"},
    )


def github_push_initial_repo(
    repo_name,
    initial_commit=["Initial scaffolding [skip ci]", "Type: trivial"],
    prompt=True,
):
    """Initializes local and remote Github repositories from a footing project

    Args:
        repo_name (str): The repository name
        initial_commit (str|List[str], optional): The initial commit message of
            the repo.
        prompt (bool, default=True): Prompt to continue on failure
    """
    remote = f"git@github.com:{GITHUB_ORG_NAME}/{repo_name}.git"
    if isinstance(initial_commit, str):
        initial_commit = [initial_commit]

    _shell("git init -b master")
    _shell("git add .")
    _shell("git commit " + " ".join(f'-m "{msg}"' for msg in initial_commit))
    _shell(f"git remote add origin {remote}")

    ret = _shell("git push origin master", check=False)
    if ret.returncode != 0:
        msg = "There was an error when pushing the initial repository."
        prompt_msg = (
            f"{msg} This could be because the initial repository has already"
            " been set up or because the repository previously existed."
            " Continue without pushing (y) or abort (n)?"
        )
        if prompt and yesno(prompt_msg, default="no"):
            raise GithubPushError(msg)


def _get_circleci_api_and_auth(repo_name):
    """Returns the CircleCI API url and auth"""
    circleci_api_token = os.environ[CIRCLECI_API_TOKEN_ENV_VAR]
    circleci_auth = requests.auth.HTTPBasicAuth(circleci_api_token, "")
    circleci_api = (
        f"https://circleci.com/api/v1.1/project/github/{GITHUB_ORG_NAME}" f"/{repo_name}"
    )
    return circleci_api, circleci_auth


def circleci_follow(repo_name):
    """Follows a repo on circleci

    Args:
        repo_name (str): The repository name
    """
    circleci_api, circleci_auth = _get_circleci_api_and_auth(repo_name)
    # Follow the repository
    resp = requests.post(f"{circleci_api}/follow", auth=circleci_auth)
    resp.raise_for_status()


def circleci_configure_project_settings(repo_name):
    """Configure circleci project settings.

    Ensures circleci only runs for pull requests and
    that redundant builds are canceled.

    Args:
        repo_name (str): The repository name
    """
    circleci_api, circleci_auth = _get_circleci_api_and_auth(repo_name)
    # Follow the repository
    resp = requests.put(
        f"{circleci_api}/settings",
        auth=circleci_auth,
        json={
            "feature_flags": {
                "build-prs-only": True,
                "build-fork-prs": True,
                "autocancel-builds": True,
            }
        },
    )
    resp.raise_for_status()


def footing_setup():
    # Make sure requests is installed
    print("Installing requests library for repository setup...")
    _shell("pip3 install requests")

    print("Checking credentials.")
    if not os.getenv(GITHUB_API_TOKEN_ENV_VAR):
        raise CredentialsError(
            f'You must set a "{GITHUB_API_TOKEN_ENV_VAR}" environment variable'
            " with repo creation permissions in order to spin up a public"
            " python library project. Create a personal access token"
            " at https://github.com/settings/tokens"
        )

    if not os.getenv(CIRCLECI_API_TOKEN_ENV_VAR):
        raise CredentialsError(
            f'You must set a "{CIRCLECI_API_TOKEN_ENV_VAR}" environment'
            " variable in order for public python library creation to work."
            " Create a token at https://circleci.com/account/api"
        )

    print(
        f"Creating the github repository at https://github.com/" f"{GITHUB_ORG_NAME}/{REPO_NAME}"
    )
    github_create_repo(REPO_NAME, DESCRIPTION)

    print("Creating initial repository and pushing to master.")
    github_push_initial_repo(REPO_NAME)

    print("Setting up default branch protection.")
    github_setup_branch_protection(
        REPO_NAME,
        "master",
        {
            "required_pull_request_reviews": None,
            "required_status_checks": {
                "contexts": [
                    "ci/circleci: check_changelog",
                    "ci/circleci: lint",
                    "ci/circleci: test",
                ],
                "strict": True,
            },
            "enforce_admins": False,
            "restrictions": None,
        },
    )

    print("Following the project on CircleCI.")
    circleci_follow(REPO_NAME)

    print("Configuring CircleCI project settings.")
    circleci_configure_project_settings(REPO_NAME)

    get_user_input(
        "Final step! Go to"
        " https://github.com/Opus10/public-django-app-template"
        "#readthedocs-setup"
        " and read the instructions for ReadTheDocs integration. If you bypass"
        ' this step, your docs will not build properly. Hit "return" after'
        " you have done this."
    )

    print(
        f'Setup complete! cd into "{REPO_NAME}", make a new branch,'
        ' and type "make docker-setup" to set up your development environment.'
    )


if __name__ == "__main__":
    # Don't allow this template to be used by other tools like cookiecutter
    if not os.getenv(FOOTING_ENV_VAR):
        print(
            "This template can only be used with footing for project spin up. "
            "Consult the footing docs at https://github.com/Opus10/footing"
        )
        sys.exit(1)

    # Ensure that footing setup only gets executed when ``_FOOTING`` is set to
    # ``setup``. This means that setup steps will not be executed by other
    # footing commands (e.g ``footing update``)
    if os.getenv(FOOTING_ENV_VAR) == "setup":
        prompt_msg = (
            f'Your Opus 10 Github repo name will be "{REPO_NAME}"'
            f' and packages will be installed with "pip install {REPO_NAME}".'
            f' Python imports will happen as "import {MODULE_NAME}".'
            " It is very difficult to change these names after the project"
            " is started, so please be sure these are the names you want!"
            " Continue (y) or change parameters (n)?"
        )
        if yesno(prompt_msg):
            footing_setup()
        else:
            print("Setup aborted. Please try again with new parameters.")
            sys.exit(1)
