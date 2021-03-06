# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werkzeug.utils import cached_property

from zaih_core.database import (
    db, Model, SurrogatePK, generator_string_id)


__all__ = [
    'Active',
]


def active_id_generator():
    return generator_string_id(20, 4)


class Active(SurrogatePK, Model):

    __tablename__ = 'active'
    __table_args__ = (
        db.Index('ix_feed_account_id_status', 'account_id', 'status'),
    )

    TARGET_TYPE_ARTICLE = 'article'
    TARGET_TYPE_POST = 'post'
    TARGET_TYPE_REPLY = 'reply'

    SOURCE_APP = 'app'
    SOURCE_WXAPP = 'wxapp'
    SOURCE_WEIXIN = 'weixin'
    SOURCE_PANEL = 'panel'

    STATUS_ACTIVE = 'active'
    STATUS_DISABLE = 'disable'

    ACTION_POST_FORWARD = 'post_forward'
    ACTION_PUBLISH_ARTICLE = 'publish_article'

    id = db.Column(db.String(32), primary_key=True, default=active_id_generator)
    account_id = db.Column(db.Integer, nullable=False, index=True)
    column_id = db.Column(db.String(32), nullable=False, index=True)
    action = db.Column(db.String(32), nullable=False, index=True)  # 触发的动作
    target_id = db.Column(db.String(32), nullable=False, index=True)  # 触发动作目标id
    target_type = db.Column(
        db.String(32), nullable=False, index=True,
        server_default=u'question')  # 触发动作目标类型
    description = db.Column(db.String(), nullable=True)
    source = db.Column(
        db.String(16), nullable=True, index=True,
        default='weixin')  # 动态来源
    status = db.Column(
        db.String(16), nullable=False, index=True,
        server_default='active')  # 当前动态状态 是否有效

    @cached_property
    def account(self):
        from sub.cache.accounts import account_meta
        account = account_meta(self.account_id)
        return account
