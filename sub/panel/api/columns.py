# -*- coding: utf-8 -*-

from flask import g

from . import Resource
from zaih_core.pager import get_offset_limit

from sub.models import Column
from sub.utils import get_slave_query
from sub.services.permissions import register_permission


class Columns(Resource):

    def get(self):
        nickname = g.args.get('nickname')

        filter_fields = ['id', 'name', 'column_id',
                         'status', 'account_id']
        query = get_slave_query(Column, filter_fields, g.args)
        if nickname:
            from sub.cache.accounts import get_account_ids_by_nickname
            ids = get_account_ids_by_nickname(nickname)
            if ids:
                query = query.filter(Column.account_id.in_(ids))
            else:
                return [], 200, [('Total-Count', str(0))]

        count = query.count()

        offset, limit = get_offset_limit(g.args)
        columns = (query
                     .order_by(Column.date_created.desc())
                     .offset(offset).limit(limit)
                     .all())
        return columns, 200, [('Total-Count', str(count))]

    def post(self):
        from sub.tasks import add_nickname_account_ids, process_after_subscribed
        g.json.update(review_status=Column.REVIEW_STATUS_AUTO_PASSED)
        column = Column.create(**g.json)
        process_after_subscribed(column.account_id, column.id)
        add_nickname_account_ids.delay(column.account_id)
        return column, 201
