# {{ cookiecutter.repo_name }}

## Compatibility

`{{ cookiecutter.repo_name }}` is compatible with Python 3.8 - 3.12{% if cookiecutter.is_django == "True" %}, Django 4.2 - 5.1, Psycopg 2 - 3, and Postgres 13 - 16{% endif %}.

## Documentation

[View the {{ cookiecutter.repo_name }} docs here](https://{{ cookiecutter.repo_name }}.readthedocs.io/)

## Installation

Install `{{ cookiecutter.repo_name }}` with:

    pip3 install {{ cookiecutter.repo_name }}

{%- if cookiecutter.is_django == "True" %}
After this, add `{{ cookiecutter.module_name }}` to the `INSTALLED_APPS` setting of your Django project.
{%- endif %}

## Contributing Guide

For information on setting up {{ cookiecutter.repo_name }} for development and contributing changes, view [CONTRIBUTING.md](CONTRIBUTING.md).
