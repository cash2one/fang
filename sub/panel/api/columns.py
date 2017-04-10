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
                         'status', 'account_id', 'review_status']
        query = get_slave_query(Column, filter_fields, g.args)
        order_by = g.args.get('order_by', 'date_created')
        count = query.count()

        offset, limit = get_offset_limit(g.args)
        order_dict = {
            'date_created': Column.date_created.desc(),
        }
        order_by = order_dict.get(order_by)
        columns = (query
                     .order_by(order_by)
                     .offset(offset).limit(limit)
                     .all())
        return columns, 200, [('Total-Count', str(count))]

    def post(self):
        column = Column.create(**g.json)
        return column, 201
