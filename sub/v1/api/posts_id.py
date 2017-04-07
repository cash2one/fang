# -*- coding: utf-8 -*-
from flask import g

from zaih_core.api_errors import NotFound, BadRequest

from sub.models import Post, Member

from . import Resource


class PostsId(Resource):

    def get(self, id):
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
        return post, 200
