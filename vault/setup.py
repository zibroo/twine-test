#!/usr/bin/env python
 
from setuptools import setup
import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"./requirements.txt"
install_requires = ['markdown==3.7','requests==2.32.3','hvac==2.3.0'] 
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()
setup(
    name='vault',
    version='7.0',
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
    python_requires='>=3.8',
    zip_safe=False
)
