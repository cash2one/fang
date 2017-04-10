# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta, datetime
from werkzeug.utils import cached_property
from sqlalchemy.ext.hybrid import hybrid_property

from flask import g
from sqlalchemy import sql

from zaih_core.ztime import now, str_time
from zaih_core.database import (db, Model, DateTime,
                                SurrogatePK, generator_string_id)


__all__ = [
    'Column',
    'Member',
    'Assistant',
]


def column_id_generator():
    return generator_string_id(18, 8)


class Column(Model):

    __tablename__ = 'column'

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'

    REVIEW_STATUS_PENDING = 'pending'           # 等待审核
    REVIEW_STATUS_PASSED = 'passed'             # 审核通过
    REVIEW_STATUS_REJECTED = 'rejected'         # 审核不通过
    REVIEW_STATUS_AUTO_PASSED = 'auto_passed'   # 自动过审

    PUBLIC_REVIEW_STATUSES = [REVIEW_STATUS_PASSED, REVIEW_STATUS_AUTO_PASSED]

    id = db.Column(
        db.String(32), primary_key=True, default=column_id_generator)
    name = db.Column(db.String(128), nullable=False, index=True)
    account_id = db.Column(db.Integer(), nullable=False, index=True)
    image = db.Column(db.String(512), nullable=True)
    price = db.Column(db.Integer(), nullable=False, index=True)
    content = db.Column(db.String(), nullable=False)
    assistant_name = db.Column(db.String(32), nullable=True)
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
    date_start = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_end = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_created = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_updated = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    @cached_property
    def account(self):
        from sub.cache.accounts import account_meta
        account = account_meta(self.account_id)
        return account

    @cached_property
    def current_is_subscribed(self):
        account_id = g.account.id if hasattr(g, 'account') else None
        if not account_id:
            return False
        from sub.cache.columns import ColumnMembers
        cm = ColumnMembers(self.id)
        return cm.is_subscribed(account_id)


class Member(SurrogatePK, Model):

    __tablename__ = 'member'
    __table_args__ = (db.UniqueConstraint('account_id', 'column_id'),)

    account_id = db.Column(db.Integer(), nullable=False, index=True)
    column_id = db.Column(db.String(32), nullable=False, index=True)


class Assistant(SurrogatePK, Model):

    __tablename__ = 'assistant'
    __table_args__ = (db.UniqueConstraint('account_id', 'column_id'),)

    account_id = db.Column(db.Integer(), nullable=False, index=True)
    column_id = db.Column(db.String(32), nullable=False, index=True)
    date_updated = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())
