from flask import url_for

from ..fixtures import *


@pytest.mark.parametrize("method,path,query_string,data,status_code", [
    ('GET', '/auth/login', '', {}, 200),
    ('GET', '/auth/logout', '', {}, 302),  # redirect to index
    ('GET', '/auth/register', '', {}, 200),
    ('GET', '/auth/reset_password_request', '', {}, 200),
])
def test_routes(method, path, query_string, data, status_code, client):
    assert client.open(method=method, path=path, query_string=query_string, data=data).status_code == status_code
