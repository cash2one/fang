# -*- coding: utf-8 -*-

from zaih_core.api_errors import NotFound

from sub.models import Column

from . import Resource


class ColumnsId(Resource):

    def get(self, id):
        column = (
            Column.query
            .filter(Column.id == id)
            .filter(~Column.is_hidden)
            .filter(Column.review_status.in_(Column.PUBLIC_REVIEW_STATUSES))
            .filter(Column.status == Column.STATUS_PUBLISHED)
            .first())
        if not column:
            raise NotFound('column_not_found')
        return column, 200
