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
    member = Member.query.filter_by(account_id=account_id, column_id=column.id).first()
    if not member:
        member = Member.create(account_id=account_id, column_id=column.id)
        from sub.cache.columns import ColumnMembers
        cm = ColumnMembers(column.id)
        cm.update_members(account_id)


@celery.task()
def process_after_paid(order_id, order=None):
    from sub.models import Order
    if not order:
        order = Order.query.get(order_id)
    if not order:
        return
    if order.status != Order.STATUS_PENDING:
        return
    order.update(status=Order.STATUS_PAID, date_updated=now())
    if order.order_type == Order.ORDER_TYPE_SUBSCRIBE_COLUMN:
        process_after_subscribed(order.account_id, order.target_id)
    return True


@celery.task()
def process_after_liking(liking_id):
    from sub.models import Liking
    from sub.cache.reply_statistics import ReplyStatistics
    liking = Liking.query.get(liking_id)
    if not liking:
        return
    if liking.target_type == Liking.TARGET_TYPE_REPLY:
        rs = ReplyStatistics(liking.target_id)
        rs.update_likings_count()


@celery.task()
def notice_after_review_reply(reply_id, reply=None):
    from sub.models import Reply
    if not reply:
        reply = Reply.query.get(reply_id)
    if not reply:
        return
    if reply.review_status not in Reply.PUBLIC_REVIEW_STATUSES:
        return
    post = reply.post
    if not post:
        return
    extras = {
        'column_id': reply.column_id,
        'post_id': reply.post_id,
        'reply_id': reply.id,
    }
    push = Push(
        'notice_reply_post', post.account_id, extras=extras)
    push.send()


@celery.task()
def process_after_review_reply(reply_id, reply=None):
    from sub.models import Reply
    from sub.cache.post_statistics import PostStatistics
    if not reply:
        reply = Reply.query.get(reply_id)
    if not reply:
        return
    if reply.review_status in Reply.PUBLIC_REVIEW_STATUSES:
        ps = PostStatistics(reply.post_id)
        ps.update_replies_count()
        notice_after_review_reply.delay(reply.id)


@celery.task()
def process_after_reply(reply_id):
    from sub.models import Reply
    reply = Reply.query.get(reply_id)
    if not reply:
        return
    if reply.review_status in Reply.PUBLIC_REVIEW_STATUSES:
        process_after_review_reply(reply_id, reply)
