# -*- coding: utf-8 -*-
from flask import g

from zaih_core.api_errors import NotFound, BadRequest
from zaih_core.pager import get_offset_limit

from sub.models import Post

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