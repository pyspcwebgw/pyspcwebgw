#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.1.1'
DOWNLOAD_URL = \
    'https://github.com/mbrrg/pyspcwebgw/archive/{}.zip'.format(VERSION)

setup(
    name='pyspcwebgw',
    packages=['pyspcwebgw'],
    version=VERSION,
    description='A Python library for communicating with SPC Web Gateway.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Martin Berg',
    author_email='mbrrg@users.noreply.github.com',
    license='MIT',
    url='https://github.com/mbrrg/pyspcwebgw',
    download_url=DOWNLOAD_URL,
    install_requires=['aiohttp', 'asynccmd'],
    python_requires='>=3.5',
    scripts=['scripts/spcwebgw-console'],
    keywords=['spc', 'vanderbilt', 'web gateway'],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: Home Automation'
    ],
)
