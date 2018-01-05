#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""stream-cli setup.py."""

import os
import sys

from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='onesignal',
    version='0.1.0',
    py_modules=['onesignal.cli', 'onesignal.config'],
    install_requires=[
        'click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        onesignal=onesignal.cli:cli
    '''
)
