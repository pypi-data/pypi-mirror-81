#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import setup, find_packages

from bapy import User, Url, path

setup(
    author=User.gecos,
    author_email=Url.email(),
    description=path.project.description(),
    entry_points={
        'console_scripts': [
            f'{path.repo} = {path.repo}:app',
        ],
    },
    include_package_data=True,
    install_requires=path.project.requirements['requirements'],
    name=path.repo,
    package_data={
        path.repo: [f'{path.repo}/scripts/*', f'{path.repo}/templates/*'],
    },
    packages=find_packages(),
    python_requires='>=3.8,<4',
    scripts=path.scripts_relative,
    setup_requires=path.project.requirements['requirements_setup'],
    tests_require=path.project.requirements['requirements_test'],
    url=Url.lumenbiomics(http=True, repo=path.repo).url,
    use_scm_version=False,
    version='0.2.141',
    zip_safe=False,
)
