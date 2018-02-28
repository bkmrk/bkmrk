import bkmrk

import pytest

from ..config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


@pytest.fixture
def app():
    app = bkmrk.create_app(TestConfig)
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
