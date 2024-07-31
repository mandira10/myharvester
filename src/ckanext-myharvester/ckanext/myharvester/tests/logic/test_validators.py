"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.myharvester.logic import validators


def test_myharvester_reauired_with_valid_value():
    assert validators.myharvester_required("value") == "value"


def test_myharvester_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.myharvester_required(None)
