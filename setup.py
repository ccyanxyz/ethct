#!/usr/bin/env python
from setuptools import setup

setup(
    name = 'ethct',
    version = '19.10.25',
    description = 'Ethereum contract tool(command line)',
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
