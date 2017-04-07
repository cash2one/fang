# -*- coding: utf-8 -*-
from flask import g
from . import Resource

from zaih_core.api_errors import NotFound

from sub.models import Reply
from sub.services.permissions import register_permission


class RepliesId(Resource):

    def _get_reply(self, id):
        reply = Reply.get_by_id(id)
        if not reply:
            raise NotFound('reply_not_found')
        return reply

    @register_permission('get_reply')
    def get(self, id):
        post = self._get_reply(id)
        return post, 200

    @register_permission('update_column')
    def put(self, id):
        reply = self._get_reply(id)
        if g.json:
            reply.update(**g.json)
        return reply, 200