#!/usr/bin/env python3
"""Checks that execute before the python project is created.

This script ensures that python package and module names are
valid.

Note that this runs during ``footing setup`` and ``footing update``
"""
import re
import sys


MODULE_REGEX = r"^[a-zA-Z][_a-zA-Z0-9]+$"
PACKAGE_REGEX = r"^[a-zA-Z][-a-zA-Z0-9]+$"

module_name = "{{ cookiecutter.module_name }}"
package_name = "{{ cookiecutter.repo_name }}"

if not re.match(MODULE_REGEX, module_name):
    print("ERROR: %s is not a valid Python module name!" % module_name)
    sys.exit(1)

if not re.match(PACKAGE_REGEX, package_name):
    print(
        f"ERROR: {package_name} is not a valid Python package name!"
        " Note: we require package names to use hyphens instead of underscores"
    )
    sys.exit(1)
