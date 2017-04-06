# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from requests.exceptions import ConnectTimeout, ReadTimeout

from sub.settings import Config
from sub.utils import generate_nonce_str


def get_wxapp_token(appid, secret, is_refresh=False):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential'
    from sub.app import memc
    memc_key = 'wxapp_access_token'
    access_token = memc.get(memc_key)
    if not access_token or access_token == 'None' or is_refresh:
        try:
            resp = requests.get(url, params={'appid': appid, 'secret': secret},
                                timeout=(2, 2))
        except (ConnectTimeout, ReadTimeout):
            return
        token = resp.json()
        access_token = token.get('access_token')
        if access_token:
            memc.set(memc_key, access_token, 3600)
    return access_token


def get_weixinmp_token(appid, is_refresh=False):
    from sub.app import memc
    from weixin import WeixinMpAPI
    from weixin.oauth2 import (ConnectTimeoutError,
                               ConnectionError,
                               OAuth2AuthExchangeError)
    token = memc.get('weixin_mp_access_token')
    errors = None
    if not token or token == 'None' or is_refresh:
        try:
            api = WeixinMpAPI(
                appid=appid, app_secret=Config.WEIXINMP_APP_SECRET,
                grant_type='client_credential')
            token = api.client_credential_for_access_token().get('access_token')
            if token:
                memc.set('weixin_mp_access_token', token, 3600)
        except (OAuth2AuthExchangeError, ConnectTimeoutError,
                ConnectionError), ex:
            errors = ex
    return token, errors


def get_weixin_jsapi_ticket(token):
    from sub.app import memc
    from weixin import WeixinMpAPI
    from weixin.oauth2 import (ConnectTimeoutError,
                               ConnectionError,
                               OAuth2AuthExchangeError)
    jsapi_ticket = memc.get('weixin_mp_jsapi_ticket')
    errors = None
    if not jsapi_ticket or jsapi_ticket == 'None':
        try:
            api = WeixinMpAPI(access_token=token)
            jsapi_ticket = api.jsapi_ticket(type='jsapi').get('ticket')
            if jsapi_ticket:
                memc.set('weixin_mp_jsapi_ticket', jsapi_ticket, 3600)
        except (OAuth2AuthExchangeError, ConnectTimeoutError,
                ConnectionError), ex:
            errors = ex
    return jsapi_ticket, errors


def weixin_mp_config(url):
    import time
    from weixin.helper import genarate_js_signature
    appid = Config.WEIXINMP_APPID
    nonce = generate_nonce_str()
    timestamp = int(time.time())
    token, errors = get_weixinmp_token(appid)
    if errors:
        message = {'error_code': errors.code,
                   'error_msg': errors.description}
        return message
    jsapi_ticket, errors = get_weixin_jsapi_ticket(token)
    if errors:
        message = {'error_code': errors.code,
                   'error_msg': errors.description}
        return message
    params = {
        'jsapi_ticket': jsapi_ticket,
        'timestamp': str(timestamp),
        'noncestr': nonce,
        'url': url
    }
    signature = genarate_js_signature(params)
    config = {
        'appId': appid,
        'timestamp': str(timestamp),
        'nonceStr': nonce,
        'signature': signature,
    }
    return config
