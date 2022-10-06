Public Django App Template
##########################

This repository provides a template for a pip-installable public Django
app deployed using CircleCI to PyPI.

This is a `cookiecutter <https://cookiecutter.readthedocs.io/en/latest/>`__
template that can be used by
`footing <https://github.com/Opus10/footing/>`__ to create and manage the
project.

A new public Django app can be started with::

    pip3 install footing
    footing setup git@github.com:Opus10/public-django-app-template.git

**Note** when calling ``footing setup``, a project will be created locally and
it will also be set up on Github and CircleCI for continuous deployment.
Do **not** create anything on Github or CircleCI before using this template.

This template assumes the user has a ``GITHUB_API_TOKEN`` environment variable
that contains a Github personal access token. Create one by going to
"https://github.com/settings/tokens" and clicking "Generate New Token".
Select the top-level "repo" checkbox as the only scope.

The template also assumes the user has a ``CIRCLECI_API_TOKEN``
environment variable that contains a personal CircleCI token. Create
one by going to "https://circleci.com/account/api" and clicking
"Create New Token". The token is used for following the repository and
configuring it with the proper settings.

The following docs cover the parameters needed for the template and more
information on how this template is used in practice.

Template Parameters
===================

When calling ``footing setup``, the user will be prompted for template
parameters. These parameters are defined in the cookiecutter.json file and are
as follows:

1. ``repo_name``: The name of the repository **and** and name that will be
   used when installing via pip. Be sure that the name isn't taken on PyPI
   before creation.
2. ``module_name``: The name of the Python module that will be imported as a
   library. Modules must have underscores
   (i.e. ``import my_installable_package``)
3. ``short_description``: A short description of the project. This will be
   added as the Github repo description and the description in the
   `setup.cfg` file. It will also be the description displayed when users do
   ``footing ls github.com/Opus10`` to list this project.

What Does This Template Provide?
================================

When using this template with
``footing setup git@github.com:Opus10/public-django-app-template.git``,
the ``hooks/pre_gen_project.py`` and ``hooks/post_gen_project.py`` files will
be called to bootstrap your Python project. The following steps are taken:
_

1. Create a local repository.
2. Create a remote Github repository for the project.
3. Optionally add collaborators to the Github repository.
4. Push the initial repository to Github.
5. Follow the project on CircleCI.

Once all of this is complete, the user can take advantage of all of the
scaffolding provided by the template, which includes:

1. Automatic deployment to PyPI when merging into the master
   (see ``.circleci/config.yaml``).
2. Flake8 integration (see ``setup.cfg`` for configuration).
3. Coverage integration (see ``setup.cfg`` for coverage configuration).
4. Automatic version tagging and version bumping (more on this in later
   sections).
5. Automatic generation of CHANGELOG.md using
   `git-tidy <https://github.com/Opus10/git-tidy>`__.
6. A makefile for setting up the development environment locally
   (``make docker-setup``), running tests (``make test``), and running linting
   (``make lint``).
7. A CircleCI file for running tests, doing deployments, and verifying any
   project made with this template remains up to date.
8. A ``.gitignore`` file with defaults for Python, Atom, Vim, Emacs,
   Git, Pycharm, Mac files, and other popular apps.
9. Scaffolding for `Sphinx <http://www.sphinx-doc.org/en/stable/index.html>`__
   documentation.
10. Commit linting during pull request review that verifies commits adhere
    to the proper schema. The linter also comments on Github pull requests
    so that reviewers can see what the release notes will look like for
    a particular pull request.

ReadTheDocs Setup
=================

This template does not automatically set up readthedocs.org integration.
In order to do that, go to https://readthedocs.org/dashboard/import/,
click "Opus 10", and refresh the repositories. Import the
project with the default values.

Once the project has been followed, go to
https://readthedocs.org/dashboard/{project_name}/rules/regex/create/
and under "version type" choose "tag" and choose "activate version"
as the rule. After this, create a new rule with the same settings,
except choose "Set version as default".

ReadTheDocs builds should happen automatically after the first version is
published.

An Important Note to Users
==========================

By using this template for your Python project, you are agreeing that you will
keep your project up to date with this template whenever it changes. You will
know that your project is out of date when CircleCI runs the
``footing update --check`` command in the ``.circleci/config.yaml`` file of the
project. When this happens, you can run ``footing update`` locally in your
project repo to pull in the latest template updates.

**Note** If you must do a release because of emergency circumstances, comment
out ``footing update --check`` in the ``.cirlceci/config.yaml`` file to
temporarily bypass the template check.

It is important to keep any changes to the templated files of this project to
a minimum, otherwise ``footing update`` will produce diffs that can be
difficult to merge. Along with that, minimally editing the templated files
ensures that your Python library project behaves similarly to all of the other
ones at Opus 10. If there is an error in the templated files or a change that
needs to be propagated to every package (e.g. updating Python), then the change
should be made in this template repository.

Please be aware that editing **any** part of this template repository
(even this README file) will cause CircleCI builds to fail for all packages
built with this template. Any changes to the template should not be taken
lightly, and ideally multiple changes are merged in at once.

Technical Decisions and How To
==============================

There are quite a few interacting pieces of this template that are described
in the following, along with a guide on how they work within the context of
your Python package.

Sphinx Documentation and Autodocs
---------------------------------

This template includes scaffolding for creating documentation with
`Sphinx <http://www.sphinx-doc.org/en/stable/index.html>`__,
a tool for creating documentation for Python code. With Sphinx, one writes
their documentation as
`ReStructured Text <http://docutils.sourceforge.net/rst.html>`__. The power
of Sphinx comes from its ability to handle
*directives* to do special tasks with documentation, such as automatically
documenting a module or running a piece of code and showing its output.

We used Sphinx and the
`Read the Docs Theme <http://docs.readthedocs.io/en/latest/theme.html>`__
for building and styling documentation because of its ubiquity in the
Python community. Along with that, we chose it because it makes documentation
beautiful and searchable, something we hoped that would make writing
documentation more fun for others.

For some examples of projects that make use of Sphinx, check out the following
documentation folders for the following:

1. `stor <https://github.com/counsyl/stor/tree/master/docs>`__
2. `footing <https://github.com/Opus10/footing/tree/master/docs>`__

Remember that one can also perform
``footing ls github.com/Opus10 git@github.com:Opus10/public-django-app-template.git`` to see a
list of all projects spun up with this template for examples at Opus 10.

Building docs also comes with this template. In order to build and look at docs
locally, one has to first set up the project with ``make docker-setup`` and then
type ``make docs`` to build docs. Docs can be opened with ``make open-docs``.

**Note** Docs are also built during ``make lint`` in order to catch any
documentation building errors during continuous integration.

Library Dependencies
--------------------

In order to add dependencies to your library, add them to ``pyproject.toml``.
Typically python packages will include dependencies in ``setup.py`` under
the ``install_requires`` attribute, but
`poetry <https://poetry.eustace.io/>`__, our python packaging library,
moves all packaging configuration out of ``setup.py`` into ``pyproject.toml``.

While it makes sense to pin dependencies in an application, non-dev
dependencies should **never** be pinned in the ``pyproject.toml`` of a Python
library. There are two primary reasons for this:

1. Assume you pin a library (e.g. ``sqlalchemy``) to 1.1.1 in your library.
   If any application uses your library, it is also now forced to use
   ``sqlalchemy==1.1.1``. Requiring any other version of ``sqlalchemy`` by that
   application will either result in a dependency conflict or in an ambiguous
   version of ``sqlalchemy`` being used by the library and by the
   application depending on how deployment is orchestrated.
2. Even if one pins a library under a certain version like ``sqlalchemy<1.3``,
   it can still cause issues. Say that a security patch was released and an
   application must now update ``sqlalchemy`` to 1.3. The problems from the
   first example will now arise, and then maintainers of the library need to
   edit its dependencies and deploy a new version before the application
   can be safely deployed.

The second option should only be used if you are **certain** that your library
breaks under a particular version of a dependency. Otherwise, one should also
leave their dependencies unpinned or use ``>=`` when specifying dependencies.

This template includes tests as part of the released library, meaning the
application has the ability to install the package and run its tests against
the requirements pinned by the application. This is the preferred way to catch
issues with libraries and their dependencies.

Versioning and Deployment
-------------------------

Typically when deploying python packages, one will manually edit the version in
a ``setup.py`` (or in our case, ``pyproject.toml``) file and then go through a
series of steps to tag the version and push it to a package server. This
template takes care of all of those steps automatically.

Version management is performed during deployment by the ``devops.py`` script
that is created with the project. It behaves in the following manner:

1. Determines the current version of the project by the version set in
   ``pyproject.toml``.
2. Parses the commits since the version tag and checks for any ``Type:``
   trailers in the commit message. Note that git trailers at the footer
   of the commit messages.
3. If any ``Type: api-break`` trailers are found, the major version will be
   updated. If any ``Type: feature`` or ``Type: bug`` trailers are found,
   the minor version will be updated. Everything else will result in a patch
   version update.
4. Poetry is used to update the version in ``pyproject.toml`` based on
   the semantic version update.
5. The repository is tagged with the new version.
6. A ``CHANGELOG.md`` file is created by
   `git-tidy <https://github.com/Opus10/git-tidy>`__.
7. The repository is committed, deployed to PyPI, and then pushed to
   github.

Pausing Deployment
^^^^^^^^^^^^^^^^^^

In order to pause deployment, either pause the CircleCI project or cancel the
build after the deploy branch is merged.


Testing and Validation
======================

Python libraries are set up to use
`pytest <http://pytest-django.readthedocs.io/en/latest/>`__ as the test runner
and framework. `coverage <https://coverage.readthedocs.io>`__ is also used to
ensure that code meets a minimum testing coverage requirement. Testing is
executed in the ``.circleci/config.yaml`` file and can be executed locally
with ``make test``.

By default, the template configures that every branch of code is covered by
tests in the ``setup.cfg`` file. It is recommended to not turn off this setting
and instead opt for placing ``# pragma: no cover`` comments on
functions or lines of code that do not have any value in being covered by tests.
By keeping this setting on, it helps ensure that any new additions to the
library have been tested or have at least been documented to say
that it isn't valuable to test.

For validation, `flake8 <http://flake8.pycqa.org/en/latest/>`__
is used to do static analysis of code. These checks are executed in the
``.circleci/config.yaml`` file and can be executed locally with
``make lint``.

FAQ
===

Why Use This Template?
----------------------

Using this template ensures that your Python package behaves like all of the
other Django apps at Opus 10, all the way from local development to
documentation to production deployment. Having all of our Django
apps set up, documented, and deployed in similar ways decreases the
cognitive load for others using, fixing, and maintaining your tool.

Using this template also ensures your package is kept up to date with changes
at Opus 10, such as when we upgrade Python to newer versions or potentially
switch to a different packaging index.
