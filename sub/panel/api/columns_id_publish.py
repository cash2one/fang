# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class ColumnsIdPublish(Resource):

    def put(self, id):
        print(g.headers)

        return {}, 200, None

    def delete(self, id):
        print(g.headers)

        return {}, 204, None