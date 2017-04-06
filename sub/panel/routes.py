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
from .api.columns_id_publish import ColumnsIdPublish


routes = [
    dict(resource=ColumnsId, urls=['/columns/<id>'], endpoint='columns_id'),
    dict(resource=Columns, urls=['/columns'], endpoint='columns'),
    dict(resource=Voices, urls=['/voices'], endpoint='voices'),
    dict(resource=ColumnsIdPublish, urls=['/columns/<id>/publish'], endpoint='columns_id_publish'),
]