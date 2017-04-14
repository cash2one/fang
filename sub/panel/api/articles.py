# -*- coding: utf-8 -*-

from flask import g
from . import Resource

from zaih_core.pager import get_offset_limit

from sub.models import Article, Column
from sub.utils import get_slave_query
from sub.services.permissions import register_permission
from zaih_core.api_errors import NotFound
from zaih_core.coding import smart_str


class Articles(Resource):

    # @register_permission('get_articles')
    def get(self):
        title = g.args.get('title')
        filter_fields = ['id', 'column_id', 'status', 'account_id']

        query = get_slave_query(Article, filter_fields, g.args)
        if title:
            query = query.filter(Article.title.like("%{}%".format(smart_str(title))))
        count = query.count()

        offset, limit = get_offset_limit(g.args)
        articles = (query
                     .order_by(Article.date_created.desc())
                     .offset(offset).limit(limit)
                     .all())
        return articles, 200, [('Total-Count', str(count))]

    # @register_permission('create_article')
    def post(self):
        column_id = g.json.get('column_id', '')
        column = (
            Column.query
            .filter(Column.id == column_id)
            .filter(~Column.is_hidden)
            .filter(Column.review_status.in_(Column.PUBLIC_REVIEW_STATUSES))
            .first())
        if not column:
            raise NotFound('column_not_found')

        g.json.update(review_status=Article.REVIEW_STATUS_AUTO_PASSED)
        article = Article.create(**g.json)
        return article, 201