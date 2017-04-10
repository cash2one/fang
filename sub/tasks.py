# -*- coding: utf-8 -*-
import random
from datetime import timedelta

import flask
from celery import Celery
from sqlalchemy.exc import IntegrityError
# from raven.contrib.celery import register_signal

from zaih_core.ztime import now, str_time
from zaih_core.helpers import get_backend_api

from sub.settings import Config
from sub.services.jpush import Push

FENDA_DOMAIN = Config.FENDA_DOMAIN
ADMIN_ID = 10000000


def make_celery():
    from sub.app import create_app
    app = create_app(register_bp=False)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            if flask.has_app_context():
                return TaskBase.__call__(self, *args, **kwargs)
            else:
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery()


@celery.task()
def send_msg(msg_type=None, mobile=None, msg=None, message=None, **extras):
    from sub.services.message import Message
    # 异步发送短信
    if message:
        message.msg_type = msg_type or message.msg_type
        message.mobile = mobile or message.mobile
        message.msg = msg or message.msg
        message.extras.update(extras)
    else:
        message = Message(msg_type, mobile, msg, **extras)
    message.send()
    return message


@celery.task()
def jpush_send(push):
    # 异步推送
    resp = push._send()
    if flask.current_app.config['DEBUG']:
        print u'jpush:%s:%s' % (push.receiver_id, push.alert)
        print push.extras
    return resp


@celery.task()
def process_after_subscribed(account_id, column_id):
    from sub.models import Column, Member
    column = Column.query.get(column_id)
    if not column:
        return
    member = Member.query.filter_by(account_id=account_id, column_id=column.id)
    if not member:
        member = Member.create(account_id=account_id, column_id=column.id)
        from sub.cache.columns import ColumnMembers
        cm = ColumnMembers(column.id)
        cm.update_members(account_id)


@celery.task()
def process_after_paid(order_id):
    from sub.models import Order
    order = Order.query.get(order_id)
    if not order:
        return
    if order.status != Order.STATUS_PENDING:
        return
    order.update(status=Order.STATUS_PAID, date_updated=now())
    if order.order_type == Order.ORDER_TYPE_SUBSCRIBE_COLUMN:
        process_after_subscribed(order.account_id, order.target_id)
