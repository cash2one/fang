# -*- coding: utf-8 -*-

from flask import g

from sub.models import Order

from . import Resource


class PayNotify(Resource):

    def post(self):
        result = {'ok': False, 'is_settle': False}
        order_id = g.json['order_id']
        status = g.json['status']
        order = Order.query.get(order_id)
        if not order:
            result.update(ok=False)
            return result, 201
        if order.status == Order.STATUS_PAID:
            result.update(ok=True)
            return result, 201
        if order.status != Order.STATUS_PENDING:
            result.update(ok=False)
            return result, 201
        if status == 'success':
            from sub.tasks import process_after_paid
            r = process_after_paid(order.id, order)
            if r:
                result.update(ok=True, is_settle=True)
        return result, 201
