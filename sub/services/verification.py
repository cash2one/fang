# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import base64

import six
import slumber
from flask import current_app as app

from zaih_core.models import ApiModel
from zaih_core.caching import cache_for
from zaih_core.helpers import get_backend_api
from zaih_core.verification import get_authorization


@cache_for(3600)
def verify_client(token):
    ALLOW_CLIENTS = app.config.get('ALLOW_CLIENTS', ['weixin'])
    client = base64.b64decode(token)
    try:
        client_id, secret = client.split(':')
    except ValueError:
        return False, None
    if not app.config['TESTING'] and client_id not in ALLOW_CLIENTS:
        return False, None
    api = get_backend_api('auth')
    scopes = api.client.scopes.post({'client_id': client_id, 'secret': secret})
    if scopes:
        scopes = scopes.get('scopes')
        if scopes:
            return True, scopes
    return False, None


class Account(ApiModel):

    def __init__(self, id, *args, **kwargs):
        self.id = id
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def __unicode__(self):
        return "Account: %s" % self.nickname


class Token(ApiModel):

    def __init__(self, access_token, *args, **kwargs):
        self.access_token = access_token
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def __unicode__(self):
        return "AccessToken: %s" % self.access_token


@cache_for(60)
def verify_token(token):
    api = slumber.API(
        app.config['FENDA_OAUTH_API'],
        auth=(app.config['APP_CLIENT_ID'],
              app.config['APP_CLIENT_SECRET']),
        append_slash=False)
    token_info = api.post({'access_token': token})
    if token_info:
        if isinstance(token_info, dict):
            return True, token_info
        try:
            token_info = json.loads(token_info)
        except ValueError:
            return False, None
    return False, None


def verify_request():
    authorization_type, token = get_authorization()
    if authorization_type == 'Basic':
        return verify_client(token)
    elif authorization_type == 'Bearer':
        return verify_token(token)
    return False, None
