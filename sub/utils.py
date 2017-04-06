# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
import string
import random
from datetime import timedelta

import requests
from requests.exceptions import ConnectTimeout, ReadTimeout

from raven.contrib.flask import Sentry

from sub.settings import Config

sentry = Sentry(register_signal=True, logging=True)


def generate_nonce_str(length=32):
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(length))


def format_amount(amount):
    return '￥%0.2f' % (amount / 100.0)


def url_with_next(endpoint, **kwargs):
    from flask import url_for, request
    next_url = request.args.get('next', None)
    kwargs.setdefault('next', next_url)
    return url_for(endpoint, **kwargs)


def filter_params(filter_fields, params):
    new_params = {k: v for k, v in params.items() if k in filter_fields}
    return new_params


def get_query(model, filter_fields, params):
    new_params = filter_params(filter_fields, params)
    return model.query.filter_by(**new_params)


def get_slave_query(model, filter_fields=[], params={}):
    from sub.services.db_routing import slave
    query = slave.session.query(model)
    if filter_fields and params:
        new_params = filter_params(filter_fields, params)
        query = query.filter_by(**new_params)
    return query


def get_msg(message, **kwargs):
    from zaih_core.coding import smart_unicode
    _kwargs = {k: smart_unicode(v) for k, v in kwargs.items()}
    message = smart_unicode(message)
    return message.format(**_kwargs)


def make_template_data(openid, template_id, url, **kwargs):
    message = {
        "touser": openid,
        "template_id": template_id,
        "url": url,
    }
    data = {}
    for k, v in kwargs.items():
        data[k] = {
            "value": v,
            "color": "#173177"
        }
    message["data"] = data
    return message


def send_template_msg(openid, template_id, url, **kwargs):
    from sub.settings import Config
    from sub.services.wxconfig import get_weixinmp_token
    appid = Config.WEIXINMP_APPID
    base_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send'
    access_token, error = get_weixinmp_token(appid)
    if error:
        return
    data = make_template_data(openid, template_id, url, **kwargs)
    try:
        resp = requests.post(base_url, params={'access_token': access_token},
                             json=data, timeout=(2, 2))
    except (ConnectTimeout, ReadTimeout):
        return
    content = resp.json()
    if content.get('errcode') == 40001:
        # 如果token 过期 自动刷新 重新发送
        get_weixinmp_token(appid, is_refresh=True)
        return send_template_msg(openid, template_id, url, **kwargs)
    return content


def error_notice(first, kw1='分答', kw2='出错了', remark='请快速处理'):
    openid = Config.ADMIN_OPENID
    template_id = Config.TEMPLATE_ID_ERROR
    send_template_msg(openid, template_id,
                      Config.APP_DOMAIN,
                      first=first,
                      keyword1=kw1,
                      keyword2=kw2,
                      remark=remark)


def filter_spam(content, filters=[]):
    from requests.auth import HTTPBasicAuth
    username = Config.REVIEW_SERVER_USERNAME
    password = Config.REVIEW_SERVER_PASSWORD
    url = Config.REVIEW_SERVER_URL
    data = {'message': content}
    if filters:
        filters = ','.join(filters)
        data.update(filters=filters)
    try:
        req = requests.post(url, data=data,
                            auth=HTTPBasicAuth(username, password),
                            timeout=(1, 1))
    except:
        req = False
    if req and req.status_code == 200:
        return req.json()
    return {}


def check_nigger(content, with_detail=False):
    res = filter_spam(content, filters=['blacklist'])
    if res:
        nigger = res.get('nigger')
        summary = res.get('nigger_summary', {})
        is_nigger = bool(nigger)
        return (is_nigger, summary) if with_detail else is_nigger
    else:
        from sub.spam_words import spam_words
        for word in spam_words:
            if word in content:
                return (True, {word: 1}) if with_detail else True
        return (False, {}) if with_detail else False


def check_spam(content):
    res = filter_spam(content, filters=['bayes'])
    if res:
        spam = res.get('spam')
        if spam == 'True' or spam is True:
            return True
    return False


def format_timedelta(diff, default='', fmt='%Y-%m-%d %H:%M', suffix='内'):
    """根据timedelta返回特定字符串"""
    if not (diff and isinstance(diff, timedelta)):
        return ''
    result = default
    total_seconds = diff.total_seconds()
    periods = (
        (total_seconds / 60, '分钟', 60),
        (total_seconds / 3600, '小时', 49),
        (total_seconds / (3600 * 24), '天', float('+inf')),
    )
    for period, unit, max_period in periods:
        period = math.ceil(period)
        if period < max_period:
            result = '%d%s' % (period, unit)
            break
    if result and suffix:
        result = '%s%s' % (result, suffix)
    return result


def make_wxapp_template_data(openid, template_id, form_id, page, **kwargs):
    message = {
        'touser': openid,
        'template_id': template_id,
        'form_id': form_id,
        'page': page,
    }
    data = {}
    for k, v in kwargs.items():
        data[k] = {
            "value": v,
            "color": "#173177"
        }
    message["data"] = data
    return message


def send_wxapp_template_msg(openid, template_id, form_id, page, **kwargs):
    from sub.settings import Config
    from sub.services.wxconfig import get_wxapp_token
    access_token = get_wxapp_token(Config.WXAPP_APPID, Config.WXAPP_SECRET)
    if not access_token:
        return
    base_url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send'
    data = make_wxapp_template_data(openid, template_id, form_id, page, **kwargs)
    try:
        resp = requests.post(base_url, params={'access_token': access_token},
                             json=data, timeout=(2, 2))
    except (ConnectTimeout, ReadTimeout):
        return
    content = resp.json()
    if content.get('errcode') == 40001:
        # 如果token 过期 自动刷新 重新发送
        get_wxapp_token(Config.WXAPP_APPID, Config.WXAPP_SECRET, is_refresh=True)
        return send_wxapp_template_msg(openid, template_id, form_id,
                                       page, **kwargs)
    return content