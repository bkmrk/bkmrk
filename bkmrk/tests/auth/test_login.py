from flask import g, url_for

from ..fixtures import *
from .. import utils


def test_login_success(client, user):
    """Test login (success)."""
    resp = utils.login_user(client, user)

    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('main.index')


def test_login_fail_no_user(client):
    """Test login failure (no user)."""
    user = {
        'username': 'nouser',
        'password': 'password',
    }
    resp = utils.login_user(client, user)

    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('auth.login')


def test_login_fail_wrong_passwd(client, user):
    user['password'] += 'a'
    resp = utils.login_user(client, user)

    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('auth.login')


def test_login_already_authenticated(client, user):
    utils.login_user(client, user)
    resp = utils.login_user(client, user)

    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('main.index')
