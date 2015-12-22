#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = ['xmltodict', 'requests']

setup(
    name='pagseguro-api-v2',
    version='0.0.2',
    description='Pagseguro API',
    author='Joffily Ferreira',
    author_email='contato@joffily.me',
    url='https://github.com/joffilyfe/pagseguro-api',
    packages=[
        'pagseguro',
    ],
    package_dir={'pagseguro': 'pagseguro'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='pagseguro, pagseguro-api')
