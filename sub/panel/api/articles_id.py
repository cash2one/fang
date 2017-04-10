# -*- coding: utf-8 -*-

from flask import g
from . import Resource

from zaih_core.api_errors import NotFound

from sub.models import Article
from sub.services.permissions import register_permission


class ArticlesId(Resource):

    def _get_article(self, id):
        column = Article.get_by_id(id)
        if not column:
            raise NotFound('article_not_found')
        return column

    # @register_permission('get_article')
    def get(self, id):
        article = self._get_article(id)
        return article, 200

    # @register_permission('update_article')
    def put(self, id):
        article = self._get_article(id)
        if g.json:
            article.update(**g.json)
        return article, 200