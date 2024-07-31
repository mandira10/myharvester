"""Tests for helpers.py."""

import ckanext.myharvester.helpers as helpers


def test_myharvester_hello():
    assert helpers.myharvester_hello() == "Hello, myharvester!"
