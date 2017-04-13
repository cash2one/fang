# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta, datetime
from werkzeug.utils import cached_property
from sqlalchemy.ext.hybrid import hybrid_property

from flask import g
from sqlalchemy import sql
from markdown2 import markdown

from zaih_core.ztime import now, str_time
from zaih_core.database import (db, Model, DateTime,
                                SurrogatePK, generator_string_id)


__all__ = [
    'Article',
]


def article_id_generator():
    return generator_string_id(20, 7)


class Article(Model):

    __tablename__ = 'article'

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'

    REVIEW_STATUS_PENDING = 'pending'           # 等待审核
    REVIEW_STATUS_PASSED = 'passed'             # 审核通过
    REVIEW_STATUS_REJECTED = 'rejected'         # 审核不通过
    REVIEW_STATUS_AUTO_PASSED = 'auto_passed'   # 自动过审

    PUBLIC_REVIEW_STATUSES = [REVIEW_STATUS_PASSED, REVIEW_STATUS_AUTO_PASSED]

    id = db.Column(
        db.String(32), primary_key=True, default=article_id_generator)
    account_id = db.Column(db.Integer(), nullable=False, index=True)
    column_id = db.Column(db.String(32), nullable=False, index=True)
    title = db.Column(db.String(128), nullable=False, index=True)
    summary = db.Column(db.String(512), nullable=False)
    content = db.Column(db.String(), nullable=False)
    status = db.Column(
        db.String(16), nullable=False, index=True, server_default=STATUS_DRAFT)
    review_status = db.Column(
        db.String(16), nullable=False, index=True,
        server_default=REVIEW_STATUS_PENDING)
    is_hidden = db.Column(
        db.Boolean(), nullable=False, index=True,
        server_default=sql.false())
    date_published = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_created = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_updated = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    _column = db.relationship(
        'Column',
        primaryjoin='Article.column_id==Column.id',
        foreign_keys='Article.column_id')

    @cached_property
    def column(self):
        return self._column

    @cached_property
    def account(self):
        from sub.cache.accounts import account_meta
        return account_meta(self.account_id)

    @cached_property
    def voice(self):
        return self._voice

    @cached_property
    def voice_id(self):
        if self._voice:
            return self._voice.id

    @cached_property
    def current_is_subscribed(self):
        account_id = g.account.id if hasattr(g, 'account') else None
        if not account_id:
            return False
        from sub.cache.columns import ColumnMembers
        cm = ColumnMembers(self.column_id)
        return cm.is_subscribed(account_id)

    @property
    def html_content(self):
        return markdown(self.content) if self.content else ''
