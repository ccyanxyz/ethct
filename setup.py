#!/usr/bin/env python
from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name = 'ethct',
    version = '19.11.3',
    description = 'Ethereum contract tool(command line)',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/ccyanxyz/ethct',
    author = 'ccyanxyz',
    author_email = 'ccyanxyz@gmail.com',
    keywords = 'ethereum contract command-line-tool',
    install_requires = ['web3>=4.2.1'],
    py_modules = ['ethct', 'constants', 'ethct_contract', 'ethct_helper'],
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'ethct=ethct:main'
        ]
    }
)
