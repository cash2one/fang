# -*- coding: utf-8 -*-

from zaih_core.api_errors import NotFound, BadRequest
from sub.models import Voice, Article

from . import Resource


class VoicesId(Resource):

    def post(self, id):
        voice = Voice.query.get(id)
        if not voice or voice.status != Voice.STATUS_SUCCEED:
            raise NotFound('voice_not_found')
        if voice.target_type == Voice.TYPE_ARTICLE:
            art = Article.query.get(voice.target_id)
            if not art:
                raise NotFound('article_not_found')
            if not art.is_available:
                raise BadRequest('article_not_available')
        return voice, 200
