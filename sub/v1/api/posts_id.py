# -*- coding: utf-8 -*-

from zaih_core.api_errors import NotFound

from sub.models import Post

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
        return post, 200
