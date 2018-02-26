from flask import url_for

from .fixtures import *


@pytest.mark.parametrize("method,route,data,status_code", [
    ('GET', '/auth/login', {}, 200),
    ('GET', '/auth/logout', {}, 302),  # redirect to index
    ('GET', '/auth/register', {}, 200),
    ('GET', '/auth/reset_password_request', {}, 200),
])
def test_route_status_codes(method, route, data, status_code, client):
    if method == 'GET':
        assert client.get(route, data=data).status_code == status_code
    if method == 'POST':
        assert client.post(route, data=data).status_code == status_code
