from flask import g, url_for

from .. import utils
from ..fixtures import *


def test_register_success(user, client):
    """Test Registration (success).

    Attempt to successfully register. Reuse user fixture.
    """
    pass


@pytest.mark.parametrize("username,email,password,password_repeat", [
    ('', 'username@email.com', 'a' * 12, 'a' * 12),
    ('1 OR 1=1;', 'username@email.com', 'a' * 12, 'a' * 12),
    ('username', '', 'a' * 12, 'a' * 12),
    ('username', 'usernameemail.com', 'a' * 12, 'a' * 12),
    ('username', 'username@email.com', 'a' * 12, 'a' * 11),
])
def test_register_fail_validators(username, email, password, password_repeat, client):
    """Test invalid registration inputs."""
    user = {
        'username': username,
        'email': email,
        'password': password,
        'password_repeat': password_repeat,
    }
    resp = utils.register_user(client, user)

    assert resp.status_code == 200


@pytest.mark.parametrize('user1,email1,user2,email2', [
    ('username', 'username@email.com', 'username', 'newuser@email.com'),
    ('username', 'username@email.com', 'newuser', 'username@email.com'),

])
def test_register_fail_existing(user1, user2, email1, email2, client):
    """Test registration with existing user/email."""
    user1 = {
        'username': user1,
        'email': email1,
        'password': 'a' * 12,
    }
    resp = utils.register_user(client, user1)

    assert resp.status_code == 302

    client.get(url_for('auth.register'))
    csrf_token = g.csrf_token
    user2 = {
        'username': user2,
        'email': email2,
        'password': 'a' * 12,
    }
    resp = utils.register_user(client, user2)

    assert resp.status_code == 200
