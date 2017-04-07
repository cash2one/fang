# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class WeixinPay(Resource):

    def post(self):
        print(g.headers)
        print(g.json)

        return {'return_code': 'something'}, 201, None