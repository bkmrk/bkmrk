import requests

import bkmrk

from flask import g, url_for

from .fixtures import *


def register_user(client, user):
    client.get(url_for('auth.register'))
    csrf_token = g.csrf_token
    payload = {
        'csrf_token': csrf_token,
        'username': user.get('username'),
        'email': user.get('email'),
        'password': user.get('password'),
        'password_repeat': user.get('password_repeat', user.get('password')),
    }
    return client.post(url_for('auth.register'), data=payload)


def login_user(client, user):
    client.get(url_for('auth.login'))
    payload = {
        'csrf_token': g.csrf_token,
        'username': user.get('username'),
        'password': user.get('password'),
    }
    return client.post(url_for('auth.login'), data=payload)


def reset_password(client, user):
    client.get(url_for('auth.reset_password_request'))
    csrf_token = g.csrf_token
    payload = {
        'csrf_token': csrf_token,
        'email': user.get('email'),
    }
    return client.post(url_for('auth.reset_password_request'), data=payload)
