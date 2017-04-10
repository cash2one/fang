# -*- coding: utf-8 -*-
from flask import g
from . import Resource

from zaih_core.api_errors import NotFound

from sub.models import Post
from sub.services.permissions import register_permission
from zaih_core.api_errors import NotFound, BadRequest


class PostsIdReview(Resource):

    # @register_permission('update_post')
    def put(self, id):
        review_action = g.json.get('review_action')
        post = Post.query.get(id)

        if not post:
            raise NotFound('post_not_found')
        if post.review_status not in [
                Post.REVIEW_STATUS_PENDING,
                Post.REVIEW_STATUS_AUTO_PASSED]:
            raise BadRequest('post_review_status_error')

        post.update(review_status=review_action)
        return {'ok': True}, 200