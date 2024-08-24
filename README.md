# Python Library Template

This repository provides a template for a pip-installable public Python project deployed using CircleCI to PyPI.

This is a [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) template that can be used by [footing](https://github.com/Opus10/footing/) to create and manage the project.

A new public project can be started with:

    pip3 install footing
    footing setup git@github.com:Opus10/python-library-template.git

**Note** when calling `footing setup`, a project will be created locally and it will also be set up on Github and CircleCI for continuous deployment. Do **not** create anything on Github or CircleCI before using this template.

This template assumes the user has a `GITHUB_API_TOKEN` environment variable that contains a Github personal access token. Create one by going to "https://github.com/settings/tokens" and clicking "Generate New Token". Select the top-level "repo" checkbox as the only scope.

The template also assumes the user has a `CIRCLECI_API_TOKEN` environment variable that contains a personal CircleCI token. Create one by going to "https://circleci.com/account/api" and clicking "Create New Token". The token is used for following the repository and configuring it with the proper settings.

The following docs cover the parameters needed for the template and more information on how this template is used in practice.

## Template Parameters

When calling `footing setup`, the user will be prompted for template parameters. These parameters are defined in the cookiecutter.json file and are as follows:

1. `repo_name`: The name of the repository **and** and name that will be used when installing via pip. Be sure that the name isn't taken on PyPI before creation.
2. `module_name`: The name of the Python module that will be imported as a library. Modules must have underscores (i.e. `import my_installable_package`)
3. `short_description`: A short description of the project. This will be added as the Github repo description and the description in the `pyproject.toml` file. It will also be the description displayed when users do `footing ls github.com/Opus10` to list this project.
4. `check_types_in_ci`: True if type checking should be a required CI check.
5. `is_django`: True if this is a Django app.

## What Does This Template Provide?

When using this template with [footing setup](git@github.com:Opus10/python-library-template.git), the `hooks/pre_gen_project.py` and `hooks/post_gen_project.py` files will be called to bootstrap your Python project. The following steps are taken:

1. Create a local repository.
2. Create a remote Github repository for the project.
3. Optionally add collaborators to the Github repository.
4. Push the initial repository to Github.
5. Follow the project on CircleCI.

Once all of this is complete, the user can take advantage of all of the scaffolding provided by the template, which includes:

1. Automatic deployment to PyPI when merging into the main (see `.circleci/config.yaml`).
2. Ruff integration (see `pyproject.toml` for configuration).
3. Coverage integration (see `pyproject.toml` for coverage configuration).
4. A makefile for setting up the development environment locally (`make docker-setup`), running tests (`make test`), and running linting (`make lint`).
5. A CircleCI file for running tests, doing deployments, and verifying any project made with this template remains up to date.
6. A `.gitignore` file with defaults for Python, Atom, Vim, Emacs, Git, Pycharm, Mac files, and other popular apps.
7. Scaffolding for [Mkdocs Material](https://squidfunk.github.io/mkdocs-material/) documentation.

## ReadTheDocs Setup

This template does not automatically set up readthedocs.org integration. In order to do that, go to https://readthedocs.org/dashboard/import/, click "Opus 10", and refresh the repositories. Import the project with the default values.

Once the project has been followed, go to https://readthedocs.org/dashboard/{project_name}/rules/regex/create/ and under "version type" choose "tag" and choose "activate version" as the rule. After this, create a new rule with the same settings, except choose "Set version as default".

ReadTheDocs builds should happen automatically after the first version is published.

## An Important Note to Users

It is important to keep any changes to the templated files of this project to a minimum, otherwise `footing update` will produce diffs that can be difficult to merge. Along with that, minimally editing the templated files ensures that your Python library project behaves similarly to all of the other ones at Opus 10. If there is an error in the templated files or a change that needs to be propagated to every package (e.g. updating Python), then the change should be made in this template repository.

## Technical Decisions and How To

There are quite a few interacting pieces of this template that are described in the following, along with a guide on how they work within the context of your Python package.

### Mkdocs Material Documentation and Autodocs

This template includes scaffolding for creating documentation with [Mkdocs and the Material theme](https://squidfunk.github.io/mkdocs-material/). We use [mkdocstrings](https://github.com/mkdocstrings/mkdocstrings) to automatically generate documentation from docstrings.

In order to serve docs locally, set up the project natively with `make conda-setup` and then type `make serve-docs` to serve docs. Docs can be viewed at `localhost:8000`.

**Note** Docs are also built during `make lint` in order to catch any documentation building errors during continuous integration.

### Library Dependencies

In order to add dependencies to your library, add them to `pyproject.toml`. Typically python packages will include dependencies in `setup.py` under the `install_requires` attribute, but [poetry](https://poetry.eustace.io/), our python packaging library, moves all packaging configuration out of `setup.py` into `pyproject.toml`.

While it makes sense to pin dependencies in an application, non-dev dependencies should **never** be pinned in the `pyproject.toml` of a Python library. There are two primary reasons for this:

1. Assume you pin a library (e.g. `sqlalchemy`) to 1.1.1 in your library. If any application uses your library, it is also now forced to use `sqlalchemy==1.1.1`. Requiring any other version of `sqlalchemy` by that application will either result in a dependency conflict or in an ambiguous version of `sqlalchemy` being used by the library and by the application depending on how deployment is orchestrated.
2. Even if one pins a library under a certain version like `sqlalchemy<1.3`, it can still cause issues. Say that a security patch was released and an application must now update `sqlalchemy` to 1.3. The problems from the first example will now arise, and then maintainers of the library need to edit its dependencies and deploy a new version before the application can be safely deployed.

The second option should only be used if you are **certain** that your library breaks under a particular version of a dependency. Otherwise, one should also leave their dependencies unpinned or use `>=` when specifying dependencies.

This template includes tests as part of the released library, meaning the application has the ability to install the package and run its tests against the requirements pinned by the application. This is the preferred way to catch issues with libraries and their dependencies.

### Versioning and Deployment

Versions are manually specified in pyproject.toml. Tagging will invoke a CI job to automatically release it on PyPI.

### Testing and Validation

Python libraries are set up to use [pytest](http://pytest-django.readthedocs.io/en/latest/) as the test runner and framework. [coverage](https://coverage.readthedocs.io) is also used to ensure that code meets a minimum testing coverage requirement. Testing is executed in the `.circleci/config.yaml` file and can be executed locally with `make test`.

By default, the template configures that every branch of code is covered by tests in the `pyproject.toml` file. It is recommended to not turn off this setting and instead opt for placing `# pragma: no cover` comments on functions or lines of code that do not have any value in being covered by tests. By keeping this setting on, it helps ensure that any new additions to the library have been tested or have at least been documented to say that it isn't valuable to test.

For validation, [ruff](https://docs.astral.sh/ruff/) is used to do static analysis of code. These checks are executed in the `.circleci/config.yaml` file and can be executed locally with `make lint`.
