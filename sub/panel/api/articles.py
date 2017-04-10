# -*- coding: utf-8 -*-

from flask import g
from . import Resource

from zaih_core.pager import get_offset_limit

from sub.models import Article
from sub.utils import get_slave_query
from sub.services.permissions import register_permission


class Articles(Resource):

    # @register_permission('get_articles')
    def get(self):
        filter_fields = ['id', 'column_id', 'article_id',
                         'status', 'account_id']
        query = get_slave_query(Article, filter_fields, g.args)
        count = query.count()

        offset, limit = get_offset_limit(g.args)
        articles = (query
                     .order_by(Article.date_created.desc())
                     .offset(offset).limit(limit)
                     .all())
        return articles, 200, [('Total-Count', str(count))]

    # @register_permission('create_article')
    def post(self):
        column = Article.create(**g.json)
        return column, 201