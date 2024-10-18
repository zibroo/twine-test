#!/usr/bin/env python
 
from setuptools import setup
 
setup(
    name='vault',
    version='1.0',
    description='Vault authentication and secret retrieval utility',
    author='JFrog',
    author_email='jfrog@jfrog.com',
    license='MIT',
    packages=['vault'],
    install_requires=[
            'markdown',
            'requests'
      ],
    python_requires='>=3.8',
    zip_safe=False
)
