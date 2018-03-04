import bkmrk

import pytest
from flask import g, url_for

from . import config
from . import utils


@pytest.fixture
def app():
    app = bkmrk.create_app(config.TestConfig)
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture
def db(app):
    bkmrk.db.create_all()
    yield bkmrk.db
    bkmrk.db.session.remove()
    bkmrk.db.drop_all()


@pytest.fixture
def client(app, db):
    with app.test_client() as c:
        return c


@pytest.fixture
def user(client):
    _user = {
        'username': 'username',
        'email': 'username@email.com',
        'password': 'a' * 12,
    }
    resp = utils.register_user(client, _user)

    assert resp.status_code == 302
    assert resp.headers.get('location') == url_for('auth.login')

    return _user
