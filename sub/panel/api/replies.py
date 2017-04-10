# -*- coding: utf-8 -*-

from flask import g

from . import Resource
from zaih_core.pager import get_offset_limit

from sub.models import Reply
from sub.utils import get_slave_query
from sub.services.permissions import register_permission


class Replies(Resource):

    # @register_permission('get_posts')
    def get(self):
        filter_fields = ['id', 'is_hidden', 'column_id', 'post_id', 'is_sticky'
                         'status', 'account_id', 'review_status']
        query = get_slave_query(Reply, filter_fields, g.args)
        order_by = g.args.get('order_by', 'date_created')
        count = query.count()

        offset, limit = get_offset_limit(g.args)
        order_dict = {
            'date_created': Reply.date_created.desc(),
        }
        order_by = order_dict.get(order_by)
        replys = (query
                     .order_by(order_by)
                     .offset(offset).limit(limit)
                     .all())
        return replys, 200, [('Total-Count', str(count))]

    # @register_permission('create_post')
    def post(self):
        g.json['review_status'] = Reply.REVIEW_STATUS_AUTO_PASSED
        reply = Reply.create(**g.json)
        return reply, 201