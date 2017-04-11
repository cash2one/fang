# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from zaih_core.database import db, Model, SurrogatePK


__all__ = [
    'Liking',
]


class Liking(SurrogatePK, Model):

    __tablename__ = 'liking'
    __table_args__ = (
        db.UniqueConstraint('account_id', 'target_id', 'target_type'),)

    TARGET_TYPE_POST = 'post'
    TARGET_TYPE_REPLY = 'reply'

    account_id = db.Column(db.Integer(), nullable=False, index=True)
    target_id = db.Column(db.String(32), nullable=False, index=True)
    target_type = db.Column(db.String(16), nullable=False, index=True)
