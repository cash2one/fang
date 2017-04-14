# -*- coding: utf-8 -*-
from flask import g

from zaih_core.api_errors import NotFound, BadRequest
from zaih_core.pager import get_offset_limit

from sub.models import Reply

from . import Resource


class PostsIdReplies(Resource):

    def get(self, id):
        query = Reply.query.filter(Reply.post_id == id)
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