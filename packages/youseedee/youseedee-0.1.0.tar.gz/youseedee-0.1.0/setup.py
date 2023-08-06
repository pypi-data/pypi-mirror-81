#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

config = {
    'name': 'youseedee',
    'author': 'Simon Cozens',
    'author_email': 'simon@simon-cozens.org',
    'url': 'https://github.com/simoncozens/youseedee',
    'description': 'Interface to the Unicode Character Database',
    'long_description': open('README.rst', 'r').read(),
    'license': 'MIT',
    'version': '0.1.0',
    'install_requires': [],
    'classifiers': [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta"

    ],
    'package_dir': {'': 'lib'},
    'packages': find_packages("lib"),
}

if __name__ == '__main__':
    setup(**config)
