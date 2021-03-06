# -*- coding: utf-8 -*-

from flask import g

from zaih_core.pager import get_offset_limit

from sub.models import Column

from . import Resource


class Columns(Resource):

    def get(self):
        query = (
            Column.query
            .filter(~Column.is_hidden)
            .filter(Column.review_status.in_(Column.PUBLIC_REVIEW_STATUSES))
            .filter(Column.status == Column.STATUS_PUBLISHED))
        count = query.count()
        offset, limit = get_offset_limit(g.args)
        columns = (
            query
            .order_by(Column.date_published.desc())
            .offset(offset)
            .limit(limit)
            .all())
        return columns, 200, [('Total-Count', str(count))]
