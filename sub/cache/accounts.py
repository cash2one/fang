# -*- coding: utf-8 -*-

from flask import g

from .caching import CacheMeta


class AccountMeta(CacheMeta):

    meta_name = '_account_meta'
    meta_ids = '_account_meta_ids'

    def _get_metadata(self, *account_ids):
        result = {}
        account_ids = filter(lambda id: id and str(id).isdigit(), account_ids)
        if not account_ids:
            return result
        from zaih_core.helpers import get_backend_api
        backend_api = get_backend_api('fenda')
        accounts = backend_api.meta.accounts.get(account_id=account_ids)
        if not accounts:
            return result
        for account in accounts:
            account_id = account.get('id')
            if account_id:
                result[account_id] = account
        return result


def account_meta(account_id):
    account_id = int(account_id)
    if (not hasattr(g, '_account_meta') or
            account_id not in set(g._account_meta.keys())):
        try:
            g._account_meta_ids.add(account_id)
        except AttributeError:
            g._account_meta_ids = set([account_id])
    account_meta = AccountMeta()
    account_dict = account_meta._meta_values(account_id)
    return account_dict


def preload_accounts_meta(ids=None, field_name='id'):
    accounts_meta = AccountMeta(ids, field_name=field_name)
    accounts_meta.preload_meta()
    return getattr(g, accounts_meta.meta_name, {})
