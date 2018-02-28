from flask import g, url_for

from .fixtures import *


@pytest.mark.parametrize("method,path,query_string,data,status_code", [
    ('GET', '/auth/login', '', {}, 200),
    ('GET', '/auth/logout', '', {}, 302),  # redirect to index
    ('GET', '/auth/register', '', {}, 200),
    ('GET', '/auth/reset_password_request', '', {}, 200),
])
def test_route_status_codes(method, path, query_string, data, status_code, client):
    assert client.open(method=method, path=path, query_string=query_string, data=data).status_code == status_code


def test_register_form(client):
    client.get('/auth/register')
    csrf_token = g.csrf_token
    payload = {
        'csrf_token': csrf_token,
        'username': 'username',
        'email': 'test@email.com',
        'password': 'a' * 12,
        'password_repeat': 'a' * 12,
    }
    resp = client.post('/auth/register', data=payload)
    assert resp.status_code == 302
