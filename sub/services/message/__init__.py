# -*- coding: utf-8 -*-

import requests
import flask

from .config import SCHEMAS


class Message(object):
    '''自定义短信对象'''

    def __init__(self, msg_type=None, mobile=None, msg=None, **extras):
        self.msg_type = msg_type
        self.mobile = mobile
        self.msg = msg
        self.extras = extras

    def get_msg(self):
        return self.msg

    def _build(self):
        if not self.msg:
            schema = SCHEMAS.get(self.msg_type)
            if schema:
                try:
                    self.msg = schema.format(**self.extras)
                except:
                    pass

    def send(self):
        # 同步发送短信
        self._build()
        if self.msg:
            use_marketing = self.extras.get('use_marketing') or False
            return send_msg(self.mobile, self.msg, use_marketing=use_marketing)


def send_msg_by_cl(mobile, message, use_marketing=False):
    # 创蓝文化短信通道
    api_uri = flask.current_app.config['CLSMS_API_URL']
    if use_marketing:
        account = flask.current_app.config['CLSMS_ACCOUNT_MARKETING']
        password = flask.current_app.config['CLSMS_PASSWORD_MARKETING']
    else:
        account = flask.current_app.config['CLSMS_ACCOUNT']
        password = flask.current_app.config['CLSMS_PASSWORD']
    data = {
        'account': account,
        'pswd': password,
        'mobile': mobile,
        'msg': message,
        'needstatus': True,
        'extno': '791',
    }
    resp = requests.post(api_uri, data=data)
    resp_content = resp.text.split('\n')
    error = resp_content[0].split(',')[1]
    result = {'error': error,
              'msg': resp_content[1] if len(resp_content) > 1 else 'error'}
    return result


def send_msg(mobile, message, use_marketing=False):
    if (flask.current_app.config['DEBUG'] and
            not flask.current_app.config['TESTING']):
        print u'sms:%s:%s' % (mobile, message)
        return 0

    resp = send_msg_by_cl(mobile, message, use_marketing)
    if int(resp.get('error')) == 0:
        # TODO: 发送成功保存短信发送记录
        pass
    return resp
