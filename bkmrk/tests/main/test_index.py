import pytest

from ..fixtures import *
from .. import utils


def test_index(client, user):
    """Test index page."""
    utils.login_user(client, user)
    resp = client.get(url_for('main.index'))
    assert resp.status_code == 200
