# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.self_columns_subscribed import SelfColumnsSubscribed
from .api.columns_id_posts import ColumnsIdPosts
from .api.posts_id_replies import PostsIdReplies
from .api.alipay import Alipay
from .api.columns_id_activities import ColumnsIdActivities
from .api.articles_id import ArticlesId
from .api.weixin_pay import WeixinPay
from .api.columns_id import ColumnsId
from .api.columns import Columns
from .api.posts_id import PostsId
from .api.posts_id_forward import PostsIdForward
from .api.liking import Liking
from .api.voices_id import VoicesId


routes = [
    dict(resource=SelfColumnsSubscribed, urls=['/self/columns/subscribed'], endpoint='self_columns_subscribed'),
    dict(resource=ColumnsIdPosts, urls=['/columns/<id>/posts'], endpoint='columns_id_posts'),
    dict(resource=PostsIdReplies, urls=['/posts/<id>/replies'], endpoint='posts_id_replies'),
    dict(resource=Alipay, urls=['/alipay'], endpoint='alipay'),
    dict(resource=ColumnsIdActivities, urls=['/columns/<id>/activities'], endpoint='columns_id_activities'),
    dict(resource=ArticlesId, urls=['/articles/<id>'], endpoint='articles_id'),
    dict(resource=WeixinPay, urls=['/weixin/pay'], endpoint='weixin_pay'),
    dict(resource=ColumnsId, urls=['/columns/<id>'], endpoint='columns_id'),
    dict(resource=Columns, urls=['/columns'], endpoint='columns'),
    dict(resource=PostsId, urls=['/posts/<id>'], endpoint='posts_id'),
    dict(resource=PostsIdForward, urls=['/posts/<id>/forward'], endpoint='posts_id_forward'),
    dict(resource=Liking, urls=['/liking'], endpoint='liking'),
    dict(resource=VoicesId, urls=['/voices/<id>'], endpoint='voices_id'),
]