# -*- coding: utf-8 -*-

from zaih_core.api_errors import NotFound, BadRequest

from sub.models import Article

from . import Resource


class ArticlesId(Resource):

    def get(self, id):
        article = (
            Article.query
            .filter(Article.id == id)
            .filter(~Article.is_hidden)
            .filter(Article.review_status.in_(Article.PUBLIC_REVIEW_STATUSES))
            .filter(Article.status == Article.STATUS_PUBLISHED)
            .first())
        if not article:
            raise NotFound('article_not_found')
        if not article.is_subscribed:
            raise BadRequest('not_subscribe_column')
        return article, 200
