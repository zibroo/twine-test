#!/usr/bin/env python
 
from setuptools import setup

setup(
    name='vault',
    version='7.3',
    description='Vault authentication and secret retrieval utility',
    author='JFrog',
    author_email='jfrog@jfrog.com',
    license='MIT',
    packages=['vault'],
    install_requires=[
            'markdown==3.7',
            'requests==2.32.3',
            'hvac==2.3.0'
      ],
    dependency_links=[
        'https://pypi.org/simple'
    ],
    python_requires='>=3.8',
    zip_safe=False
)
