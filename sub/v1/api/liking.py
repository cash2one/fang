# -*- coding: utf-8 -*-

from flask import g

from zaih_core.api_errors import BadRequest

from sub.models import Liking as LikingModel

from . import Resource


class Liking(Resource):

    def post(self):
        g.json['account_id'] = g.account.id
        liking = LikingModel.query.filter_by(**g.json).first()
        if liking:
            raise BadRequest('already_liking')
        liking = LikingModel.create(**g.json)
        return liking, 201
