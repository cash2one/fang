# -*- coding: utf-8 -*-

from flask import g

from zaih_core.api_errors import NotFound, BadRequest
from zaih_core.pager import get_offset_limit

from sub.models import Post, Column

from . import Resource


class ColumnsIdPosts(Resource):

    def get(self, id):
        query = (
            Post.query
            .filter(~Post.is_hidden)
            .filter(Post.column_id == id)
            .filter(Post.review_status.in_(Post.PUBLIC_REVIEW_STATUSES)))
        count = query.count()
        offset, limit = get_offset_limit(g.args)
        posts = (
            query
            .order_by(Post.is_sticky.desc())
            .order_by(Post.date_updated.desc())
            .offset(offset)
            .limit(limit)
            .all())
        return posts, 200, [('Total-Count', str(count))]

    def post(self, id):
        column = (
            Column.query
            .filter(Column.id == id)
            .filter(~Column.is_hidden)
            .filter(Column.review_status.in_(Column.PUBLIC_REVIEW_STATUSES))
            .filter(Column.status == Column.STATUS_PUBLISHED)
            .first())
        if not column:
            raise NotFound('column_not_found')
        if column.account_id != g.account.id:
            raise BadRequest("can_not_post")
        g.json.update(
            account_id=g.account.id,
            column_id=column.id,
            review_status=Post.REVIEW_STATUS_AUTO_PASSED)
        post = Post.create(**g.json)
        return post, 201
