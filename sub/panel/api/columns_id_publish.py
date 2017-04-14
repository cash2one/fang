# -*- coding: utf-8 -*-

from . import Resource

from zaih_core.ztime import now
from zaih_core.api_errors import NotFound, BadRequest

from sub.models import Column
from sub.services.permissions import register_permission


class ColumnsIdPublish(Resource):

    def _get_column(self, id):
        column = Column.query.get(id)
        if not column:
            raise NotFound('column_not_found')
        return column

    def put(self, id):
        column = self._get_column(id)
        if column.is_hidden or (column.status not in [Column.STATUS_DRAFT]):
            raise BadRequest('column_status_error')

        params = {
            'status': Column.STATUS_PUBLISHED
        }
        if not column.date_published:
            params['date_published'] = now()
        column.update(**params)
        return column, 200

    def delete(self, id):
        column = self._get_column(id)
        column.update(status=Column.STATUS_DRAFT)
        return {}, 204