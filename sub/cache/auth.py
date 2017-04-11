# -*- codking: utf-8 -*-
from __future__ import unicode_literals

from flask import g
from requests.exceptions import ConnectTimeout, ReadTimeout, ConnectionError


class Authentication(object):

    def __init__(self, account_id):
        self.account_id = account_id
        self.akey = 'account:%s:authentications' % account_id

    def get_all(self):
        auths = getattr(g, self.akey, None)
        if auths is None:
            from zaih_core.helpers import get_backend_api
            backend_api = get_backend_api('auth')
            try:
                auths = backend_api.accounts(self.account_id).auths.get(timeout=(1, 1))
                if isinstance(auths, dict):
                    # if account not found
                    return {}
            except (ConnectTimeout, ReadTimeout, ConnectionError):
                return {}
        else:
            return auths
        kwargs = {}
        for auth in auths:
            kwargs['account_id'] = auth.get('account_id')
            kwargs[auth['approach']] = auth['identity']
        setattr(g, self.akey, kwargs)
        return kwargs

    def get_single(self, approach):
        auths = self.get_all()
        identity = auths.get(approach, None)
        return identity
