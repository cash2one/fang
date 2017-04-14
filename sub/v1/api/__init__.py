# -*- coding: utf-8 -*-
from __future__ import absolute_import

import flask_restful as restful

from ..validators import request_validate, response_filter
from ..helpers import login_option


class Resource(restful.Resource):
    method_decorators = [request_validate, login_option, response_filter]
