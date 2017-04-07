# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import g

from zaih_core.api_errors import NotFound, BadRequest

from sub.services.media import media_saveas
from sub.services.permissions import register_permission
from sub.models import Article, Voice

from . import Resource


class Voices(Resource):

    def _get_article(self, id):
        article = Article.query.get(id)
        if not article:
            raise NotFound('article_not_found')
        return article

    @register_permission('get_article')
    def get(self):
        article_id = g.args.get('article_id')
        voices = (Voice.query
                  .filter(Voice.target_id == article_id)
                  .filter(Voice.target_type == Voice.TYPE_ARTICLE))
        return voices, 200

    @register_permission('update_article')
    def post(self):
        article_id = g.json['article_id']
        source = g.json['source']
        voice = Voice.create(source=source,
                             target_type=Voice.TYPE_ARTICLE, target_id=article_id)
        media_key = media_saveas(source)
        if not media_key:
            raise BadRequest('voice_error')
        voice.update(voice_key=media_key)

        return voice, 201
