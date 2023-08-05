#!/usr/bin/env python
# -*- coding:utf-8 -*-

import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='zylogger', 
    version='0.0.1', 
    author='robin zhang', 
    author_email='lit050528@gmail.com', 
    description='A logger can be used directly', 
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url='https://github.com/nicolerobin/zylogger', 
    packages=setuptools.find_packages(), 
    classifiers=[
    ], 
    python_requires='>=2.7', 
)
