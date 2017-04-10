# -*- coding: utf-8 -*-
from flask import g
from . import Resource

from zaih_core.api_errors import NotFound

from sub.models import Post
from sub.services.permissions import register_permission


class PostsId(Resource):

    def _get_post(self, id):
        post = Post.query.get(id)
        if not post:
            raise NotFound('post_not_found')
        return post

    # @register_permission('get_post')
    def get(self, id):
        post = self._get_post(id)
        return post, 200

    # @register_permission('update_column')
    def put(self, id):
        post = self._get_post(id)
        if g.json:
            post.update(**g.json)
        return post, 200