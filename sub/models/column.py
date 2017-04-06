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
]


def recourse_id_generator():
    return generator_string_id(18, 1)


class Column(Model):

    __tablename__ = 'column'
