# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class PostsId(Resource):

    def get(self, id):
        print(g.headers)

        return {}, 200, None

    def put(self, id):
        print(g.headers)
        print(g.json)

        return {}, 200, None