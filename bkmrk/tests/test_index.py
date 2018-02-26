import pytest

from .fixtures import *


def test_routes(client):
    resp = client.get('/index')
    assert resp.status_code == 302  # redirect because not logged in
