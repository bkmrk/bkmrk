import re

from flask import g, url_for

import bkmrk

from ..fixtures import *
from .. import utils


@pytest.mark.parametrize('email', [
    ('username@email.com'),
    ('whodat@email.com'),
])
def test_any_email(email, client, user):
    """Test any valid email redirects to login page.

    Even if the email is not in the database, we want to redirect to the login
    page so we do not leak which emails are registered.
    """
    client.get(url_for('auth.reset_password_request'))
    csrf_token = g.csrf_token
    payload = {
        'csrf_token': csrf_token,
        'email': email,
    }
    resp = client.post(url_for('auth.reset_password_request'), data=payload)

    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('auth.login')


def test_reset_password(client, user):
    with bkmrk.mail.record_messages() as outbox:
        utils.reset_password(client, user)
        assert len(outbox) == 1
        body = outbox[0].body
    m = re.search(r'(?P<url>http.*)', body)
    url = m.groupdict().get('url')

    resp = client.get(url)
    csrf_token = g.csrf_token
    new_password = 'b' * 12
    payload = {
        'csrf_token': csrf_token,
        'password': new_password,
        'password_repeat': new_password,
    }
    resp = client.post(url, data=payload)

    user['password'] = new_password
    resp = utils.login_user(client, user)
    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('main.index')


def test_reset_password_already_authenticated(client, user):
    utils.login_user(client, user)
    resp = utils.reset_password(client, user)

    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('main.index')
