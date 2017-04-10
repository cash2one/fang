# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.columns_id_posts import ColumnsIdPosts
from .api.posts_id_replies import PostsIdReplies
from .api.replies import Replies
from .api.articles_id_publish import ArticlesIdPublish
from .api.replies_id import RepliesId
from .api.articles import Articles
from .api.articles_id import ArticlesId
from .api.posts_id_review import PostsIdReview
from .api.columns_id import ColumnsId
from .api.columns import Columns
from .api.posts_id import PostsId
from .api.columns_id_publish import ColumnsIdPublish
from .api.posts import Posts
from .api.replies_id_review import RepliesIdReview
from .api.voices import Voices


routes = [
    dict(resource=ColumnsIdPosts, urls=['/columns/<id>/posts'], endpoint='columns_id_posts'),
    dict(resource=PostsIdReplies, urls=['/posts/<id>/replies'], endpoint='posts_id_replies'),
    dict(resource=Replies, urls=['/replies'], endpoint='replies'),
    dict(resource=ArticlesIdPublish, urls=['/articles/<id>/publish'], endpoint='articles_id_publish'),
    dict(resource=RepliesId, urls=['/replies/<id>'], endpoint='replies_id'),
    dict(resource=Articles, urls=['/articles'], endpoint='articles'),
    dict(resource=ArticlesId, urls=['/articles/<id>'], endpoint='articles_id'),
    dict(resource=PostsIdReview, urls=['/posts/<id>/review'], endpoint='posts_id_review'),
    dict(resource=ColumnsId, urls=['/columns/<id>'], endpoint='columns_id'),
    dict(resource=Columns, urls=['/columns'], endpoint='columns'),
    dict(resource=PostsId, urls=['/posts/<id>'], endpoint='posts_id'),
    dict(resource=ColumnsIdPublish, urls=['/columns/<id>/publish'], endpoint='columns_id_publish'),
    dict(resource=Posts, urls=['/posts'], endpoint='posts'),
    dict(resource=RepliesIdReview, urls=['/replies/<id>/review'], endpoint='replies_id_review'),
    dict(resource=Voices, urls=['/voices'], endpoint='voices'),
]