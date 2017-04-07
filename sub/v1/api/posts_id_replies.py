# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class PostsIdReplies(Resource):

    def get(self, id):
        print(g.headers)
        print(g.args)

        return [], 200, None

    def post(self, id):
        print(g.headers)
        print(g.json)

        return {}, 201, None