#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for memefryer.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""
from pytest import fixture
import os

@fixture
def datadir():

   return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'resources',
)