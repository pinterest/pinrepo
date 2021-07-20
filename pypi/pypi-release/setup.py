#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

__version__ = '1.0.2'
markdown_contents = open(os.path.join(os.path.dirname(__file__),
                                      'README.rst')).read()

setup(
    name='pypi-release',
    version=__version__,
    description='Release pypi package to Pinrepo',
    long_description=markdown_contents,
    url='https://github.com/pinterest/pinrepo',
    license='Apache License 2.0',
    install_requires=['boto'],
    entry_points={
        'console_scripts': [
            'pypi-release = pypi_release.pypi_release:main'
        ],
    },
    author="Baogang Song",
    author_email="baogang@pinterest.com",
    keywords='pypi pinrepo pinterest artifact repository',
    packages=['pypi_release']
)
