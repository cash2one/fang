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
    'Order',
]


def order_id_generator():
    return generator_string_id(20, 2)


class Order(Model):

    __tablename__ = 'order'

    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'

    id = db.Column(
        db.String(32), primary_key=True, default=order_id_generator)
    account_id = db.Column(db.Integer(), nullable=False, index=True)
    column_id = db.Column(db.Integer(), nullable=False, index=True)
    price = db.Column(db.Integer(), nullable=False, index=True)
    status = db.Column(
        db.String(16), nullable=False, index=True,
        server_default=STATUS_PENDING)
    date_created = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_updated = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())
