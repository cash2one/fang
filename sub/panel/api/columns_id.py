# -*- coding: utf-8 -*-

from flask import g
from . import Resource

from zaih_core.api_errors import NotFound

from sub.models import Column
from sub.services.permissions import register_permission


class ColumnsId(Resource):

    def _get_column(self, id):
        column = Column.get_by_id(id)
        if not column:
            raise NotFound('column_not_found')
        return column

    @register_permission('get_column')
    def get(self, id):
        column = self._get_column(id)
        return column, 200

    @register_permission('update_column')
    def put(self, id):
        column = self._get_column(id)
        if g.json:
            column.update(**g.json)
        return column, 200
