# -*- coding: utf-8 -*-
from flask import g

from zaih_core.helpers import get_backend_api
from zaih_core.api_errors import NotFound, BadRequest

from sub.models import Column, Member, Order
from sub.tasks import process_after_paid
from sub.cache.auth import Authentication

from . import Resource


def prepare_prepay_info():
    target_id = g.json['target_id']
    target_type = g.json['target_type']
    order_type = g.json['order_type']
    trade_type = g.json.get('trade_type', 'NATIVE')
    order = (
        Order.query
        .filter(Order.account_id == g.account.id)
        .filter(Order.target_id == target_id)
        .filter(Order.target_type == target_type)
        .filter(Order.order_type == order_type)
        .first())
    if order:
        if order.status == Order.STATUS_PAID:
            raise BadRequest('already_paid_success')
    if order_type == Order.ORDER_TYPE_SUBSCRIBE:
        # 订阅
        column = Column.query.get(target_id)
        if not column:
            raise NotFound('column_not_found')
        member = (
            Member.query
            .filter(Member.account_id == g.account.id)
            .filter(Member.column_id == column.id)
            .first())
        if member:
            raise BadRequest('already_subscribed')
        total_fee = column.price
        body = u'购买订阅产品《{name}》'.format(name=column.name)
    else:
        raise BadRequest('order_type_error')
    if not order:
        order = Order.create(
            account_id=g.account.id,
            target_id=target_id,
            target_type=target_type,
            order_type=order_type,
            price=total_fee)
    result = {
        'body': body,
        'trade_type': trade_type,
        'order_type': order_type,
        'order_id': order.id,
        'total_fee': total_fee,
        'account_id': g.account.id}
    if trade_type == 'JSAPI':
        auth = Authentication(g.account.id)
        openid = auth.get_single('weixin_mp')
        if openid:
            result.update(openid=openid)
    return result


class WeixinPay(Resource):

    def post(self):
        '''
        参数：
        target_id           商品id
        target_type         商品类型（column）
        order_type          订单类型（subscribe)
        trade_type          交易类型
        '''
        pay_info = prepare_prepay_info()
        bank_api = get_backend_api('bank')
        res = bank_api.wxpay.post(pay_info)
        if not res or not isinstance(res, dict):
            raise BadRequest('server_error')
        error_code = res.get('error_code')
        if error_code:
            if error_code == 'already_paid':
                process_after_paid.delay(pay_info['order_id'])
            raise BadRequest(**res)
        return res, 201
