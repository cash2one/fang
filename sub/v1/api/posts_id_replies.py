# -*- coding: utf-8 -*-

from flask import g

from zaih_core.api_errors import NotFound, BadRequest
from zaih_core.pager import get_offset_limit

from sub.models import Post, Reply

from . import Resource


class PostsIdReplies(Resource):

    def get(self, id):
        query = (
            Reply.query
            .filter(~Reply.is_hidden)
            .filter(Reply.post_id == id)
            .filter(Reply.review_status.in_(Reply.PUBLIC_REVIEW_STATUSES)))
        count = query.count()
        offset, limit = get_offset_limit(g.args)
        replies = (
            query
            .order_by(Reply.is_sticky.desc())
            .order_by(Reply.date_updated)
            .offset(offset)
            .limit(limit)
            .all())
        return replies, 200, [('Total-Count', str(count))]

    def post(self, id):

        return {}, 201, None
