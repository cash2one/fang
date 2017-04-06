# -*- coding: utf-8 -*-
from zaih_core.ztime import now
from zaih_core.api_errors import NotFound, BadRequest

from sub.models import Column
from sub.services.permissions import register_permission

from . import Resource
from .. import schemas


class ColumnsIdPublish(Resource):

    def _get_column(self, id):
        column = Column.get_by_id(id)
        if not column:
            raise NotFound('column_not_found')
        return column

    @register_permission('update_column')
    def put(self, id):
        column = self._get_column(id)
        if column.status == Column.STATUS_HIDDEN:
            raise BadRequest('column_hidden')
        params = {
            'status': Column.STATUS_PUBLISHED
        }
        if not column.date_published:
            params['date_published'] = now()
        column.update(**params)
        return column, 200

    @register_permission('update_column')
    def delete(self, id):
        column = self._get_column(id)
        column.update(status='draft')
        return {}, 204