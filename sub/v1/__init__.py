# -*- coding: utf-8 -*-
from flask import Blueprint, g
import flask_restful as restful

from sub.cache.accounts import account_meta
from sub.services.verification import verify_request
from sub.services.verification import Account

from .routes import routes
from .validators import security


@security.scopes_loader
def current_scopes():
    valid, token_info = verify_request()
    if valid and token_info:
        if isinstance(token_info, list):
            scopes = set(token_info) - set(['open'])
            return list(scopes)
        client_id = token_info.get('client_id', 'weixin')
        setattr(g, 'token_client_id', client_id)
        account_info = account_meta(token_info.get('account_id'))
        g.account = Account(**account_info)
        return token_info.get('scopes', [])
    return []

bp = Blueprint('v1', __name__, static_folder='static')
api = restful.Api(bp, catch_all_404s=False)

for route in routes:
    api.add_resource(route.pop('resource'), *route.pop('urls'), **route)
