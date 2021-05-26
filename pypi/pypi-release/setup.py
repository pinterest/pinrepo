#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

__version__ = '1.0.1'
markdown_contents = open(os.path.join(os.path.dirname(__file__),
                                      'README.rst')).read()

DEV_REQUIREMENTS = {"": ["flake8"], "3.6": ["black", "isort"]}

setup(
    name='pypi-release',
    version=__version__,
    description='Release pypi package to Pinrepo',
    long_description=markdown_contents,
    url='https://github.com/pinterest/pinrepo',
    license='Apache License 2.0',
    install_requires=['boto'],
    extras_require={
        "dev": [
            (dep + ';python_version>="' + py_version + '"') if py_version else dep
            for py_version, deps in DEV_REQUIREMENTS.items()
            for dep in deps
        ]
    },
    entry_points={
        "console_scripts": ["pypi-release = pypi_release.__main__:main"],
    },
    author="Baogang Song",
    author_email="baogang@pinterest.com",
    keywords='pypi pinrepo pinterest artifact repository',
    packages=['pypi_release']
)
