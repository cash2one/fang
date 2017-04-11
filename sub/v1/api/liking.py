# -*- coding: utf-8 -*-

from flask import g

from zaih_core.api_errors import BadRequest, NotFound

from sub.models import Liking as LikingModel, Reply, Member

from . import Resource


class Liking(Resource):

    def post(self):
        g.json['account_id'] = g.account.id
        liking = LikingModel.query.filter_by(**g.json).first()
        if liking:
            raise BadRequest('already_liking')
        if g.json['target_type'] == 'reply':
            reply = Reply.query.get(g.json['target_id'])
            if not reply:
                raise NotFound('reply_not_found')
            member = (
                Member.query
                .filter(Member.account_id == g.account.id)
                .filter(Member.column_id == reply.column_id)
                .first())
            if not member:
                raise BadRequest('not_subscribe_column')
            liking = LikingModel.create(**g.json)
        return liking, 201
