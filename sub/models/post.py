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
    'Post',
    'Reply',
]


def post_id_generator():
    return generator_string_id(20, 6)


class Post(Model):

    __tablename__ = 'post'

    REVIEW_STATUS_PENDING = 'pending'           # 等待审核
    REVIEW_STATUS_PASSED = 'passed'             # 审核通过
    REVIEW_STATUS_REJECTED = 'rejected'         # 审核不通过
    REVIEW_STATUS_AUTO_PASSED = 'auto_passed'   # 自动过审

    PUBLIC_REVIEW_STATUSES = [REVIEW_STATUS_PASSED, REVIEW_STATUS_AUTO_PASSED]

    id = db.Column(
        db.String(32), primary_key=True, default=post_id_generator)
    account_id = db.Column(db.Integer(), nullable=False, index=True)
    column_id = db.Column(db.String(32), nullable=False, index=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(), nullable=True)
    review_status = db.Column(
        db.String(16), nullable=False, index=True,
        server_default=REVIEW_STATUS_PENDING)
    is_sticky = db.Column(
        db.Boolean(), nullable=False, index=True,
        server_default=sql.false())
    is_hidden = db.Column(
        db.Boolean(), nullable=False, index=True,
        server_default=sql.false())
    date_created = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_updated = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())


def reply_id_generator():
    return generator_string_id(21, 5)


class Reply(Model):

    __tablename__ = 'reply'

    REVIEW_STATUS_PENDING = 'pending'           # 等待审核
    REVIEW_STATUS_PASSED = 'passed'             # 审核通过
    REVIEW_STATUS_REJECTED = 'rejected'         # 审核不通过
    REVIEW_STATUS_AUTO_PASSED = 'auto_passed'   # 自动过审

    PUBLIC_REVIEW_STATUSES = [REVIEW_STATUS_PASSED, REVIEW_STATUS_AUTO_PASSED]

    id = db.Column(
        db.String(32), primary_key=True, default=reply_id_generator)
    account_id = db.Column(db.Integer(), nullable=False, index=True)
    column_id = db.Column(db.String(32), nullable=False, index=True)
    post_id = db.Column(db.String(32), nullable=False, index=True)
    content = db.Column(db.String(), nullable=False)
    review_status = db.Column(
        db.String(16), nullable=False, index=True,
        server_default=REVIEW_STATUS_PENDING)
    is_sticky = db.Column(
        db.Boolean(), nullable=False, index=True,
        server_default=sql.false())
    is_hidden = db.Column(
        db.Boolean(), nullable=False, index=True,
        server_default=sql.false())
    date_created = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_updated = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())
