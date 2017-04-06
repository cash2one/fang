# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.columns_id import ColumnsId
from .api.columns import Columns
from .api.voices import Voices
from .api.articles_id_publish import ArticlesIdPublish
from .api.columns_id_publish import ColumnsIdPublish
from .api.articles import Articles
from .api.articles_id import ArticlesId


routes = [
    dict(resource=ColumnsId, urls=['/columns/<id>'], endpoint='columns_id'),
    dict(resource=Columns, urls=['/columns'], endpoint='columns'),
    dict(resource=Voices, urls=['/voices'], endpoint='voices'),
    dict(resource=ArticlesIdPublish, urls=['/articles/<id>/publish'], endpoint='articles_id_publish'),
    dict(resource=ColumnsIdPublish, urls=['/columns/<id>/publish'], endpoint='columns_id_publish'),
    dict(resource=Articles, urls=['/articles'], endpoint='articles'),
    dict(resource=ArticlesId, urls=['/articles/<id>'], endpoint='articles_id'),
]