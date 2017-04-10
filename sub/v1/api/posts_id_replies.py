# -*- coding: utf-8 -*-

from flask import g

from zaih_core.api_errors import NotFound, BadRequest
from zaih_core.pager import get_offset_limit

from sub.models import Post, Reply, Member

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
        post = (
            Post.query
            .filter(Post.id == id)
            .filter(~Post.is_hidden)
            .filter(Post.review_status.in_(Post.PUBLIC_REVIEW_STATUSES))
            .first())
        if not post:
            raise NotFound('post_not_found')
        member = (
            Member.query
            .filter(Member.account_id == g.account.id)
            .filter(Member.column_id == post.column_id)
            .first())
        if not member:
            raise BadRequest('not_subscribe_column')
        reply = Reply.create(
            account_id=g.account.id,
            column_id=post.column_id,
            post_id=post.id,
            content=g.json['content'],
            review_status=Reply.REVIEW_STATUS_AUTO_PASSED)
        return reply, 201
