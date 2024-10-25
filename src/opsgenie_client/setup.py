#!/usr/bin/env python
 
from setuptools import setup
 

setup(
    name='opsgenie_client',
    version='9.0',
    description='Opsgenie Client used to send alerts',
    url='https://github.vianttech.com/techops/opsgenie-client',
    author='JFrog',
    author_email='jfrog@jfrog.com',
    license='MIT',
    packages=['opsgenie'],
    install_requires=[
            'markdown',
            'requests'
      ],
    python_requires='>=3.8',
    zip_safe=False
)


