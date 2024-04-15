# Installation

Install `{{ cookiecutter.repo_name }}` with:

    pip3 install {{ cookiecutter.repo_name }}

{% if cookiecutter.is_django == "True" -%}
After this, add `{{ cookiecutter.module_name }}` to the `INSTALLED_APPS` setting of your Django project.
{%- endif %}