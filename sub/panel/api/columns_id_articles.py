# -*- coding: utf-8 -*-
from flask import g

from zaih_core.pager import get_offset_limit
from sub.utils import get_slave_query
from sub.models import Article
from zaih_core.coding import smart_str

from . import Resource


class ColumnsIdArticles(Resource):

    def get(self, id):
        title = g.args.get('title')
        status = g.args.get('status')

        query = (
            Article.query
            .filter(Article.column_id == id))

        if title:
            query = query.filter(Article.title.like("%{}%".format(smart_str(title))))
        elif status:
            query = query.filter(Article.status == status)

        count = query.count()
        offset, limit = get_offset_limit(g.args)
        articles = (
            query
            .order_by(Article.date_created.desc())
            .offset(offset)
            .limit(limit)
            .all())
        return articles, 200, [('Total-Count', str(count))]