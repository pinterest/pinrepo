#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

__version__ = '1.0.0'
markdown_contents = open(os.path.join(os.path.dirname(__file__),
                                      'README.md')).read()

setup(
    name='pypi-release',
    version=__version__,
    long_description=markdown_contents,
    install_requires=['boto'],
    entry_points={
        'console_scripts': [
            'pypi-release = pypi_release.pypi_release:main'
        ],
    },
    author="Baogang Song",
    author_email="baogang@pinterest.com",
    packages=['pypi_release']
)
