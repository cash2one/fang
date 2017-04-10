# -*- coding: utf-8 -*-

from flask import g

from . import Resource
from zaih_core.pager import get_offset_limit

from sub.models import Reply, Post, Column, Member
from sub.utils import get_slave_query
from sub.services.permissions import register_permission
from zaih_core.api_errors import NotFound, BadRequest


class Replies(Resource):

    # @register_permission('get_posts')
    def get(self):
        filter_fields = ['id', 'is_hidden', 'column_id', 'post_id',
                         'is_sticky', 'account_id', 'review_status']
        query = get_slave_query(Reply, filter_fields, g.args)
        count = query.count()

        offset, limit = get_offset_limit(g.args)
        replys = (query
                     .order_by(Reply.date_created.desc())
                     .offset(offset).limit(limit)
                     .all())
        return replys, 200, [('Total-Count', str(count))]

    # @register_permission('create_post')
    def post(self):
        column_id = g.json.get('column_id')
        post_id = g.json.get('post_id')
        account_id = g.json.get('account_id')

        column = (
            Column.query
            .filter(Column.id == column_id)
            .filter(~Column.is_hidden)
            .filter(Column.status == Column.STATUS_PUBLISHED)
            .first())
        if not column:
            raise NotFound('column_not_found')

        post = (
            Post.query
            .filter(Post.id == post_id)
            .filter(~Post.is_hidden)
            .filter(Post.review_status.in_(Post.PUBLIC_REVIEW_STATUSES))
            .first())
        if not post:
            raise NotFound('post_not_found')

        member = (
            Member.query
            .filter(Member.column_id == column.id)
            .filter(Member.account_id == account_id)
            .first())
        if not member:
            raise BadRequest('not_subscribe_column')

        g.json['review_status'] = Reply.REVIEW_STATUS_AUTO_PASSED
        reply = Reply.create(**g.json)
        return reply, 201