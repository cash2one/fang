# -*- coding: utf-8 -*-
from flask import g

from zaih_core.pager import get_offset_limit
from zaih_core.api_errors import NotFound, BadRequest

from sub.models import Active, Article, Post, Column

from . import Resource


class ColumnsIdActivities(Resource):

    def get(self, id):
        column = (
            Column.query
            .filter(Column.id == id)
            .filter(~Column.is_hidden)
            .filter(Column.review_status.in_(Column.PUBLIC_REVIEW_STATUSES))
            .filter(Column.status == Column.STATUS_PUBLISHED)
            .first())
        if not column:
            raise NotFound('column_not_found')
        if not column.current_is_subscribed:
            raise BadRequest('not_subscribe_column')
        query = (
            Active.query
            .filter(Active.column_id == id)
            .filter(Active.status == Active.STATUS_ACTIVE))
        count = query.count()
        offset, limit = get_offset_limit(g.args)
        acitvities = (
            query
            .order_by(Active.date_created.desc())
            .offset(offset)
            .limit(limit)
            .all())
        article_ids = []
        post_ids = []
        for a in acitvities:
            if a.target_type == Active.TARGET_TYPE_ARTICLE:
                article_ids.append(a.target_id)
            elif a.target_type == Active.TARGET_TYPE_POST:
                post_ids.append(a.target_id)
        articles = (
            Article.query
            .filter(Article.id.in_(article_ids))
            .filter(~Article.is_hidden)
            .filter(Article.review_status.in_(Article.PUBLIC_REVIEW_STATUSES))
            .filter(Article.status == Article.STATUS_PUBLISHED)
            .all()) if article_ids else []
        articles_dict = {a.id: a for a in articles}
        posts = (
            Post.query
            .filter(Post.id.in_(post_ids))
            .filter(~Post.is_hidden)
            .filter(Post.review_status.in_(Post.PUBLIC_REVIEW_STATUSES))
            .all()) if post_ids else []
        posts_dict = {p.id: p for p in posts}
        results = []
        for a in acitvities:
            if a.target_type == Active.TARGET_TYPE_ARTICLE:
                article = articles_dict.get(a.target_id)
                if article:
                    a.article = article
                    results.append(a)
            elif a.target_type == Active.TARGET_TYPE_POST:
                post = posts_dict.get(a.target_id)
                if post:
                    a.post = post
                    results.append(a)
        return results, 200, [('Total-Count', str(count))]
