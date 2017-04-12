# -*- coding: utf-8 -*-

from zaih_core.helpers import get_backend_api
from zaih_core.api_errors import BadRequest

from sub.tasks import process_after_paid

from . import Resource
from .weixin_pay import prepare_prepay_info


class Alipay(Resource):

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
        res = bank_api.alipay.post(pay_info)
        if not res or not isinstance(res, dict):
            raise BadRequest('server_error')
        error_code = res.get('error_code')
        if error_code:
            if error_code == 'already_paid':
                process_after_paid.delay(pay_info['order_id'])
            raise BadRequest(**res)
        return res, 201
