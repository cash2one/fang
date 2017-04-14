# -*- coding: utf-8 -*-

# TODO: datetime support

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###


DefinitionsCreatereply = {'required': ['content'], 'properties': {'content': {'type': 'string'}}}
DefinitionsVoicelite = {'properties': {'duration': {'type': 'integer'}, 'id': {'type': 'string'}}}
DefinitionsCreateweixinpay = {'required': ['order_type', 'trade_type', 'target_type', 'target_id'], 'properties': {'trade_type': {'default': 'NATIVE', 'enum': ['JSAPI', 'NATIVE', 'APP', 'MWEB'], 'type': 'string'}, 'target_id': {'type': 'string'}, 'order_type': {'enum': ['subscribe'], 'type': 'string', 'description': u'\u8ba2\u5355\u7c7b\u578b \u8ba2\u9605\u4e13\u680f'}, 'target_type': {'enum': ['column'], 'type': 'string'}}}
DefinitionsUnifiedorder = {'required': ['return_code'], 'properties': {'trade_type': {'enum': ['JSAPI', 'NATIVE', 'APP'], 'type': 'string'}, 'prepay_id': {'type': 'string'}, 'nonce_str': {'type': 'string'}, 'return_code': {'enum': ['SUCCESS', 'FAIL'], 'type': 'string'}, 'return_msg': {'type': 'string', 'description': u'\u9519\u8bef\u539f\u56e0'}, 'sign': {'type': 'string'}, 'device_info': {'type': 'string'}, 'mch_type': {'enum': ['guokr', 'zaihang'], 'type': 'string'}, 'err_code_des': {'type': 'string'}, 'appid': {'type': 'string'}, 'time_stamp': {'type': 'string'}, 'mweb_url': {'type': 'string'}, 'code_url': {'type': 'string', 'description': u'trade_type\u4e3aNATIVE\u662f\u6709\u8fd4\u56de'}, 'result_code': {'enum': ['SUCCESS', 'FAIL'], 'type': 'string', 'description': u'\u4e1a\u52a1\u7ed3\u679c'}, 'err_code': {'type': 'string'}}}
DefinitionsCreatealipay = {'required': ['order_type', 'target_type', 'target_id', 'trade_type'], 'properties': {'trade_type': {'default': 'alipay', 'enum': ['alipay'], 'type': 'string'}, 'target_id': {'type': 'string'}, 'order_type': {'enum': ['subscribe'], 'type': 'string', 'description': u'\u8ba2\u5355\u7c7b\u578b \u8ba2\u9605\u4e13\u680f'}, 'return_url': {'type': 'string'}, 'target_type': {'enum': ['column'], 'type': 'string'}}}
DefinitionsCreatepostactivity = {'required': ['description'], 'properties': {'description': {'type': 'string'}}}
DefinitionsSuccess = {'properties': {'ok': {'type': 'boolean'}}}
DefinitionsCreateliking = {'required': ['target_id', 'target_type'], 'properties': {'target_id': {'type': 'string'}, 'target_type': {'enum': ['post', 'reply'], 'type': 'string'}}}
DefinitionsAlipayorderreturn = {'required': ['payment_url'], 'properties': {'payment_url': {'type': 'string'}}}
DefinitionsCreatepost = {'required': ['title', 'description'], 'properties': {'description': {'type': 'string'}, 'title': {'type': 'string'}}}
DefinitionsVoice = {'properties': {'url': {'type': 'string'}, 'duration': {'type': 'integer'}, 'id': {'type': 'string'}}}
DefinitionsDatetime = {'type': 'string', 'format': 'datetime'}
DefinitionsAccount = {'properties': {'nickname': {'type': 'string'}, 'title': {'type': 'string'}, 'is_verified': {'type': 'boolean'}, 'id': {'type': 'string'}, 'avatar': {'type': 'string'}}}
DefinitionsError = {'properties': {'text': {'type': 'string'}, 'message': {'type': 'string'}, 'error_code': {'type': 'string'}}}
DefinitionsPost = {'properties': {'account': DefinitionsAccount, 'description': {'type': 'string'}, 'is_sticky': {'type': 'boolean'}, 'date_updated': DefinitionsDatetime, 'title': {'type': 'string'}, 'column_id': {'type': 'string'}, 'date_created': DefinitionsDatetime, 'replies_count': {'type': 'integer'}, 'id': {'type': 'string'}, 'account_id': {'type': 'integer'}}}
DefinitionsColumn = {'properties': {'account': DefinitionsAccount, 'assistant_name': {'type': 'string'}, 'account_id': {'type': 'integer'}, 'date_updated': DefinitionsDatetime, 'image': {'type': 'string'}, 'date_start': DefinitionsDatetime, 'content': {'type': 'string'}, 'date_published': DefinitionsDatetime, 'date_end': DefinitionsDatetime, 'date_created': DefinitionsDatetime, 'price': {'type': 'integer'}, 'id': {'type': 'string'}, 'name': {'type': 'string'}}}
DefinitionsReply = {'properties': {'account': DefinitionsAccount, 'account_id': {'type': 'integer'}, 'is_sticky': {'type': 'boolean'}, 'date_updated': DefinitionsDatetime, 'is_liked': {'type': 'boolean'}, 'column_id': {'type': 'string'}, 'content': {'type': 'string'}, 'post_id': {'type': 'string'}, 'likings_count': {'type': 'integer'}, 'date_created': DefinitionsDatetime, 'id': {'type': 'string'}}}
DefinitionsArticle = {'properties': {'account_id': {'type': 'integer'}, 'title': {'type': 'string'}, 'date_updated': DefinitionsDatetime, 'summary': {'type': 'string'}, 'column_id': {'type': 'string'}, 'content': {'type': 'string'}, 'date_created': DefinitionsDatetime, 'voice': DefinitionsVoicelite, 'id': {'type': 'string'}}}
DefinitionsColumndetail = {'properties': {'html_content': {'type': 'string'}, 'is_subscribed': {'type': 'boolean'}, 'subscribes_count': {'type': 'integer'}}, 'allOf': [DefinitionsColumn, {'type': 'object'}]}
DefinitionsPostdetail = {'allOf': [DefinitionsPost, {'type': 'object'}]}
DefinitionsArticledetail = {'properties': {'html_content': {'type': 'string'}, 'account': DefinitionsAccount}, 'allOf': [DefinitionsArticle, {'type': 'object'}]}
DefinitionsActivity = {'properties': {'account': DefinitionsAccount, 'description': {'type': 'string'}, 'date_updated': DefinitionsDatetime, 'target_id': {'type': 'string'}, 'target_type': {'enum': ['post', 'article'], 'type': 'string'}, 'date_created': DefinitionsDatetime, 'action': {'enum': ['publish_article', 'post_forward'], 'type': 'string'}, 'article': DefinitionsArticle, 'post': DefinitionsPost, 'id': {'type': 'string'}, 'account_id': {'type': 'integer'}}}

validators = {
    ('self_columns_subscribed', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}}}},
    ('columns_id_posts', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatepost},
    ('columns_id_posts', 'GET'): {'headers': {'required': [], 'properties': {'Authorization': {'required': False, 'type': 'string'}}}, 'args': {'required': [], 'properties': {'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}}}},
    ('posts_id_replies', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatereply},
    ('posts_id_replies', 'GET'): {'headers': {'required': [], 'properties': {'Authorization': {'required': False, 'type': 'string'}}}, 'args': {'required': [], 'properties': {'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}}}},
    ('alipay', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatealipay},
    ('columns_id_activities', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}}}},
    ('articles_id', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('weixin_pay', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreateweixinpay},
    ('columns_id', 'GET'): {'headers': {'required': [], 'properties': {'Authorization': {'required': False, 'type': 'string'}}}},
    ('columns', 'GET'): {'headers': {'required': [], 'properties': {'Authorization': {'required': False, 'type': 'string'}}}, 'args': {'required': [], 'properties': {'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 10000}}}},
    ('posts_id', 'GET'): {'headers': {'required': [], 'properties': {'Authorization': {'required': False, 'type': 'string'}}}},
    ('posts_id_forward', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatepostactivity},
    ('liking', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreateliking},
    ('voices_id', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
}

filters = {
    ('self_columns_subscribed', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsColumn, 'type': 'array'}}},
    ('columns_id_posts', 'POST'): {201: {'headers': None, 'schema': DefinitionsPost}},
    ('columns_id_posts', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsPost, 'type': 'array'}}},
    ('posts_id_replies', 'POST'): {201: {'headers': None, 'schema': DefinitionsReply}},
    ('posts_id_replies', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsReply, 'type': 'array'}}},
    ('alipay', 'POST'): {201: {'headers': None, 'schema': DefinitionsAlipayorderreturn}},
    ('columns_id_activities', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsActivity, 'type': 'array'}}},
    ('articles_id', 'GET'): {200: {'headers': None, 'schema': DefinitionsArticledetail}},
    ('weixin_pay', 'POST'): {201: {'headers': None, 'schema': DefinitionsUnifiedorder}},
    ('columns_id', 'GET'): {200: {'headers': None, 'schema': DefinitionsColumndetail}},
    ('columns', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsColumn, 'type': 'array'}}},
    ('posts_id', 'GET'): {200: {'headers': None, 'schema': DefinitionsPostdetail}},
    ('posts_id_forward', 'POST'): {201: {'headers': None, 'schema': DefinitionsActivity}},
    ('liking', 'POST'): {201: {'headers': None, 'schema': DefinitionsSuccess}},
    ('voices_id', 'POST'): {201: {'headers': None, 'schema': DefinitionsVoice}},
}

scopes = {
    ('self_columns_subscribed', 'GET'): ['open'],
    ('columns_id_posts', 'POST'): ['open'],
    ('posts_id_replies', 'POST'): ['open'],
    ('alipay', 'POST'): ['open'],
    ('columns_id_activities', 'GET'): ['open'],
    ('articles_id', 'GET'): ['open'],
    ('weixin_pay', 'POST'): ['open'],
    ('posts_id_forward', 'POST'): ['open'],
    ('liking', 'POST'): ['open'],
    ('voices_id', 'POST'): ['open'],
}


class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value, get_first=True):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    results = normalize(schema, value, type_defaults)
    if get_first:
        return results[0]
    return results


def normalize(schema, data, required_defaults=None):

    import six

    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            return getattr(self.data, key, default)

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

        def keys(self):
            if isinstance(self.data, dict):
                return list(self.data.keys())
            return list(vars(self.data).keys())

        def get_check(self, key, default=None):
            if isinstance(self.data, dict):
                value = self.data.get(key, default)
                has_key = key in self.data
            else:
                try:
                    value = getattr(self.data, key)
                except AttributeError:
                    value = default
                    has_key = False
                else:
                    has_key = True
            return value, has_key

    def _normalize_dict(schema, data):
        result = {}
        if not isinstance(data, DataWrapper):
            data = DataWrapper(data)

        for key, _schema in six.iteritems(schema.get('properties', {})):
            # set default
            type_ = _schema.get('type', 'object')

            # get value
            value, has_key = data.get_check(key)
            if has_key:
                result[key] = _normalize(_schema, value)
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                if type_ in required_defaults:
                    result[key] = required_defaults[type_]
                else:
                    errors.append(dict(name='property_missing',
                                       message='`%s` is required' % key))

        for _schema in schema.get('allOf', []):
            rs_component = _normalize(_schema, data)
            rs_component.update(result)
            result = rs_component

        additional_properties_schema = schema.get('additionalProperties', False)
        if additional_properties_schema:
            aproperties_set = set(data.keys()) - set(result.keys())
            for pro in aproperties_set:
                result[pro] = _normalize(additional_properties_schema, data.get(pro))

        return result

    def _normalize_list(schema, data):
        result = []
        if hasattr(data, '__iter__') and not isinstance(data, dict):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize(schema, data):
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
        }
        type_ = schema.get('type', 'object')
        if not type_ in funcs:
            type_ = 'default'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors

