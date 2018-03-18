import pytest

from flask import url_for

from ..fixtures import *
from .. import utils


def test_user(client, user):
    """Test user page."""
    utils.login_user(client, user)
    resp = client.get(url_for('main.user', username='username'))
    assert resp.status_code == 200


def test_user_nonexistent(client, user):
    """Test getting a nonexistent user."""
    utils.login_user(client, user)
    resp = client.get(url_for('main.user', username='nobody'))
    assert resp.status_code == 404
