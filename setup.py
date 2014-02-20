#!/usr/bin/env python

import os
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

test_requirements = []
with open('./requirements.txt') as requirements_txt:
    requirements = [line for line in requirements_txt]


setup(
    name='docket',
    version='0.1',
    description='composed Dockerfiles',
    packages=['docket', ],
    install_requires=requirements + test_requirements,
    long_description=open('README.md').read(),
    author='Albert Choi',
    author_email='albert.choi@gmail.com',
    entry_points = {
        'console_scripts': [
            'docket = docket.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
)
