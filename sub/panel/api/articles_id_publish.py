# -*- coding: utf-8 -*-

from . import Resource

from zaih_core.ztime import now
from zaih_core.api_errors import NotFound, BadRequest

from sub.models import Article
from sub.services.permissions import register_permission


class ArticlesIdPublish(Resource):

    def _get_article(self, id):
        column = Article.get_by_id(id)
        if not column:
            raise NotFound('column_not_found')
        return column

    @register_permission('update_article')
    def put(self, id):
        article = self._get_article(id)
        if article.is_hidden:
            raise BadRequest('article_hidden')
        params = {
            'status': Article.STATUS_PUBLISHED
        }
        if not article.date_published:
            params['date_published'] = now()
        article.update(**params)
        return article, 200

    @register_permission('update_article')
    def delete(self, id):
        article = self._get_article(id)
        article.update(status='draft')
        return {}, 204