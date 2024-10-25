#!/usr/bin/env python
 
from setuptools import setup
 

 
setup(
    name='db_query',
    version='9.0',
    description='Utility for querying a database',
    author='JFrog',
    author_email='jfrog@jfrog.com',
    license='MIT',
    packages=['db_query'],
    install_requires=[
            'markdown',
            'requests'
      ],
    python_requires='>=3.8',
    zip_safe=False
)


