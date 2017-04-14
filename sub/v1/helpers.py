# -*- coding: utf-8 -*-

from functools import wraps
from flask import g

from sub.cache.accounts import account_meta
from sub.services.verification import verify_request, Account


def login_option(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not hasattr(g, 'account'):
            valid, token = verify_request()
            if valid and token:
                if not isinstance(token, list):
                    account_info = account_meta(token.get('account_id'))
                    g.account = Account(**account_info)
        return view(*args, **kwargs)
    return wrapper
