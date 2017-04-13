# -*- coding: utf-8 -*-

from flask import g

from . import Resource
from zaih_core.pager import get_offset_limit

from sub.models import Post, Column, Member
from sub.utils import get_slave_query
from sub.services.permissions import register_permission
from zaih_core.api_errors import NotFound, BadRequest


class Posts(Resource):

    # @register_permission('get_posts')
    def get(self):
        filter_fields = ['id', 'is_hidden', 'is_sticky', 'column_id',
                         'account_id', 'review_status']
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
        column_id = g.json.get('column_id')
        account_id = g.json.get('account_id')

        column = (
            Column.query
            .filter(Column.id == column_id)
            .filter(~Column.is_hidden)
            .filter(Column.status == Column.STATUS_PUBLISHED)
            .filter(Column.review_status.in_(Column.PUBLIC_REVIEW_STATUSES))
            .first())
        if not column:
            raise NotFound('column_not_found')

        member = (
            Member.query
            .filter(Member.column_id == column.id)
            .filter(Member.account_id == account_id)
            .first())
        if not member:
            raise BadRequest('not_subscribe_column')

        g.json['review_status'] = Post.REVIEW_STATUS_AUTO_PASSED
        post = Post.create(**g.json)
        return post, 201