"""Tests for views.py."""

import pytest

import ckanext.myharvester.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "myharvester")
@pytest.mark.usefixtures("with_plugins")
def test_myharvester_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("myharvester.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, myharvester!"
