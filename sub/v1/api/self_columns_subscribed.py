# -*- coding: utf-8 -*-

from flask import g
from sqlalchemy.sql import expression

from zaih_core.pager import get_offset_limit

from sub.models import Column, Member

from . import Resource


class SelfColumnsSubscribed(Resource):

    def get(self):
        query = (
            Column.query
            .filter(Column.id == Member.column_id)
            .filter(Member.account_id == g.account.id)
            .filter(~Column.is_hidden)
            .filter(Column.review_status.in_(Column.PUBLIC_REVIEW_STATUSES))
            .filter(Column.status == Column.STATUS_PUBLISHED))
        count = query.count()
        offset, limit = get_offset_limit(g.args)
        columns = (
            query
            .order_by(expression.case((
                (Column.account_id == g.account.id, 1),
            )))
            .order_by(Column.date_published.desc())
            .offset(offset)
            .limit(limit)
            .all())
        return columns, 200, [('Total-Count', str(count))]
