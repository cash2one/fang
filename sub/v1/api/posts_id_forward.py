# -*- coding: utf-8 -*-
from flask import g

from zaih_core.api_errors import NotFound, BadRequest
from zaih_core.utils import get_client

from sub.models import Active, Post

from . import Resource


class PostsIdForward(Resource):

    def post(self, id):
        post = (
            Post.query
            .filter(Post.id == id)
            .filter(~Post.is_hidden)
            .filter(Post.review_status.in_(Post.PUBLIC_REVIEW_STATUSES))
            .first())
        if not post:
            raise NotFound("post_not_found")
        column = post.column
        if not column:
            raise NotFound("column_not_found")
        if column.account_id != g.account.id:
            raise BadRequest("can_not_forward")
        activity = Active.create(
            account_id=g.account.id,
            column_id=column.id,
            action=Active.ACTION_POST_FORWARD,
            target_id=post.id,
            target_type=Active.TARGET_TYPE_POST,
            description=g.json.get('description'),
            source=get_client())
        return activity, 201
