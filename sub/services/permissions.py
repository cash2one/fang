# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import wraps

from flask import g, abort

from zaih_core.helpers import get_backend_api


def get_account_permission_codes(account_id):
    backend = get_backend_api('account')
    codes = backend.accounts(account_id).permissions.get()
    return codes


def check_permission(code, account_id):
    permission_codes = get_account_permission_codes(account_id)
    return code in permission_codes


def register_permission(code):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            permission_codes = get_account_permission_codes(g.account.id)
            if (code not in permission_codes and
                    'superman' not in permission_codes):
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
