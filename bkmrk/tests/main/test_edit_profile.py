import pytest

from flask import url_for

from ..fixtures import *
from .. import utils


def test_edit_profile_get(client, user):
    """Test getting /edit_profile page."""
    utils.login_user(client, user)
    resp = client.get(url_for('main.edit_profile'))
    assert resp.status_code == 200


def test_edit_profile_post(client, user):
    utils.login_user(client, user)
    client.get(url_for('main.edit_profile'))
    payload = {
        'csrf_token': g.csrf_token,
        'username': user.get('username'),
        'about_me': 'This is all about me.',
    }
    resp = client.post(url_for('main.edit_profile'), data=payload)
    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('main.user', username=user.get('username'))


def test_edit_profile_post_existing_username(client, user):
    """Test case for username changing to an existing username."""
    user1 = {
        'username': 'user1',
        'email': 'user1@email.com',
        'password': 'a' * 12,
        'password_repeat': 'a' * 12,
    }
    utils.register_user(client, user1)

    utils.login_user(client, user)
    client.get(url_for('main.edit_profile'))
    payload = {
        'csrf_token': g.csrf_token,
        'username': 'user1',
        'about_me': 'This is all about me.',
    }
    resp = client.post(url_for('main.edit_profile'), data=payload)
    assert resp.status_code == 200  # Stay on the edit profile page
