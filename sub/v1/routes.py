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


routes = [
    dict(resource=ColumnsId, urls=['/columns/<id>'], endpoint='columns_id'),
    dict(resource=Columns, urls=['/columns'], endpoint='columns'),
]