# -*- coding: utf-8 -*-

from flask import g

from . import Resource
from zaih_core.pager import get_offset_limit

from sub.models import Column
from sub.utils import get_slave_query
from sub.services.permissions import register_permission


class Columns(Resource):

    def get(self):
        filter_fields = ['id', 'name', 'column_id',
                         'status', 'account_id']
        query = get_slave_query(Column, filter_fields, g.args)
        count = query.count()

        offset, limit = get_offset_limit(g.args)
        columns = (query
                     .order_by(Column.date_created.desc())
                     .offset(offset).limit(limit)
                     .all())
        return columns, 200, [('Total-Count', str(count))]

    def post(self):
        g.json.update(review_status=Column.REVIEW_STATUS_AUTO_PASSED)
        column = Column.create(**g.json)
        return column, 201
