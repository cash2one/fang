# -*- coding: utf-8 -*-

from flask import g

from . import Resource
from zaih_core.pager import get_offset_limit

from sub.models import Post
from sub.utils import get_slave_query
from sub.services.permissions import register_permission

class Posts(Resource):

    # @register_permission('get_posts')
    def get(self):
        filter_fields = ['id', 'is_hidden', 'is_sticky', 'column_id',
                         'is_sticky', 'account_id', 'review_status']
        query = get_slave_query(Post, filter_fields, g.args)
        count = query.count()

        offset, limit = get_offset_limit(g.args)
        posts = (query
                     .order_by(Post.date_created.desc())
                     .offset(offset).limit(limit)
                     .all())
        return posts, 200, [('Total-Count', str(count))]

    # @register_permission('create_post')
    def post(self):
        g.json['review_status'] = Post.REVIEW_STATUS_AUTO_PASSED
        post = Post.create(**g.json)
        return post, 201