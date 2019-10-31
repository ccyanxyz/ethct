#!/usr/bin/env python
from setuptools import setup

with open('readme.md', 'r') as f:
    long_description = f.read()

setup(
    name = 'ethct',
    version = '19.10.31.4',
    description = 'Ethereum contract tool(command line)',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/ccyanxyz/ethct',
    author = 'ccyanxyz',
    author_email = 'ccyanxyz@gmail.com',
    keywords = 'ethereum contract command-line-tool',
    install_requires = ['web3>=4.2.1'],
    py_modules = ['ethct', 'constants', 'ethct_contract'],
    entry_points = {
        'console_scripts': [
            'ethct=ethct:main'
        ]
    }
)
