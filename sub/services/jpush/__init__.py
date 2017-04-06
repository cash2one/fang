# -*- coding: utf-8 -*-

import copy
import json
try:
    import cPickle as pickle
except:
    import pickle

import jpush
import flask

from sub.app import redis
from .config import ALERTS


def jpush_create_push(alert, platform=None, audience=None, extras=None, **kwargs):
    """构造一个push并返回"""
    # alert是unicode，不能用unicode?
    alert = alert.encode('utf-8')
    app_key = flask.current_app.config['JPUSH_APP_KEY']
    master_secret = flask.current_app.config['JPUSH_MASTER_SECRET']
    _jpush = jpush.JPush(app_key, master_secret)

    push = _jpush.create_push()
    # 获取需要推送的平台，默认为空
    push.platform = platform
    # 需要推送的用户慎重起见，默认为空
    push.audience = audience

    ios_msg = jpush.ios(alert=alert, badge="+1",
                        sound="default", extras=extras)
    android_msg = jpush.android(alert='', extras=extras)
    push.notification = jpush.notification(alert=alert, ios=ios_msg,
                                           android=android_msg)
    if flask.current_app.config['DEBUG']:
        # 测试环境发推送给测试机
        push.options = {"time_to_live": 86400, "apns_production": False}
    return push


class Push(object):
    """自定义push处理和发送"""

    def __init__(self, push_type, receiver_id, alert=None,
                 alert_args={}, extras={}, platform=None, audience=None,
                 message_type=None, **kwargs):
        self.push_type = push_type
        self.receiver_id = receiver_id
        self.platform = platform or 'all'
        self.audience = audience or {'alias': [self.receiver_id]}
        self.alert_args = copy.deepcopy(alert_args)
        self.alert = alert
        # extras里包含需要给移动端返回的字段
        self.extras = copy.deepcopy(extras)
        self.message_type = message_type or push_type
        # jpush的push对象
        self.push = None
        # push 所需所有参数
        self.push_args = []
        self.push_kwargs = {}
        self.is_build = False

    def _format(self):
        if not self.alert:
            self.alert = ALERTS.get(self.push_type)
            if self.alert_args:
                self.alert = self.alert.format(**self.alert_args)

    def _build(self):
        if self.is_build:
            return
        # 主要处理alert
        self.extras['alert'] = self.alert
        self.extras = {
            'data': json.dumps(self.extras),
            'message_type': self.message_type,
        }
        self.push_args = [self.alert, self.platform, self.audience]
        self.push_kwargs = self.extras
        self.push = jpush_create_push(self.alert, self.platform,
                                      self.audience, self.extras)
        self.is_build = True

    @property
    def payload(self):
        try:
            return self.push.payload
        except AttributeError:
            return {}

    def _send(self):
        self._format()
        self._build()
        redis_key = pickle.dumps((self.push_args, self.push_kwargs))
        if redis.get(redis_key):
            return
        try:
            redis.setex(redis_key, 3600, True)
            return self.push.send()
        except jpush.JPushFailure as e:
            return e

    def send(self, **kwargs):
        from sub.tasks import jpush_send
        jpush_send.apply_async(args=[self], **kwargs)
