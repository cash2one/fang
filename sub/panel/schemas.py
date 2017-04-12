# -*- coding: utf-8 -*-

# TODO: datetime support

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###


DefinitionsCreatereply = {'properties': {'content': {'type': 'string'}, 'post_id': {'type': 'string'}, 'account_id': {'type': 'integer'}, 'column_id': {'type': 'string'}}}
DefinitionsVoicelite = {'properties': {'duration': {'type': 'string'}, 'id': {'type': 'string'}}}
DefinitionsSuccess = {'properties': {'ok': {'type': 'boolean'}}}
DefinitionsCreatearticle = {'properties': {'content': {'type': 'string'}, 'title': {'type': 'string'}, 'column_id': {'type': 'string'}, 'account_id': {'type': 'integer'}, 'summary': {'type': 'string'}}}
DefinitionsUpdatearticle = {'properties': {'status': {'enum': ['draft', 'published'], 'type': 'string'}, 'content': {'type': 'string'}, 'account_id': {'type': 'integer'}, 'title': {'type': 'string'}, 'is_hidden': {'type': 'boolean'}, 'column_id': {'type': 'string'}, 'summary': {'type': 'string'}}}
DefinitionsAccount = {'properties': {'nickname': {'type': 'string'}, 'title': {'type': 'string'}, 'is_verified': {'type': 'boolean'}, 'id': {'type': 'string'}, 'avatar': {'type': 'string'}}}
DefinitionsCreatepost = {'properties': {'title': {'type': 'string'}, 'description': {'type': 'string'}, 'account_id': {'type': 'integer'}, 'column_id': {'type': 'string'}}}
DefinitionsVoice = {'properties': {'url': {'type': 'string'}, 'duration': {'type': 'string'}, 'article_id': {'type': 'string'}, 'id': {'type': 'string'}}}
DefinitionsCreatevoice = {'properties': {'media_id': {'type': 'string'}, 'article_id': {'type': 'string'}, 'source': {'type': 'string'}}}
DefinitionsDatetime = {'type': 'string', 'format': 'datetime'}
DefinitionsNone = {'type': 'object'}
DefinitionsError = {'properties': {'text': {'type': 'string'}, 'message': {'type': 'string'}, 'error_code': {'type': 'string'}}}
DefinitionsUpdatepost = {'properties': {'description': {'type': 'string'}, 'is_sticky': {'type': 'boolean'}, 'title': {'type': 'string'}, 'review_status': {'enum': ['pending', 'passed', 'rejected', 'auto_passed'], 'type': 'string'}, 'column_id': {'type': 'string'}, 'date_published': DefinitionsDatetime, 'is_hidden': {'type': 'boolean'}, 'account_id': {'type': 'integer', 'format': 'int32'}}}
DefinitionsCreatecolumn = {'properties': {'status': {'enum': ['draft', 'published'], 'type': 'string'}, 'name': {'type': 'string'}, 'image': {'type': 'string'}, 'date_start': DefinitionsDatetime, 'content': {'type': 'string'}, 'price': {'type': 'integer'}, 'date_end': DefinitionsDatetime, 'account_id': {'type': 'integer'}}}
DefinitionsArticlelite = {'properties': {'status': {'type': 'string'}, 'date_published': DefinitionsDatetime, 'account': DefinitionsAccount, 'title': {'type': 'string'}, 'date_created': DefinitionsDatetime, 'id': {'type': 'string'}}}
DefinitionsUpdatereply = {'properties': {'account_id': {'type': 'integer', 'format': 'int32'}, 'is_sticky': {'type': 'boolean'}, 'review_status': {'enum': ['pending', 'passed', 'rejected', 'auto_passed'], 'type': 'string'}, 'column_id': {'type': 'string'}, 'content': {'type': 'string'}, 'post_id': {'type': 'string'}, 'is_hidden': {'type': 'boolean'}, 'date_published': DefinitionsDatetime}}
DefinitionsReply = {'properties': {'content': {'type': 'string'}, 'date_published': DefinitionsDatetime, 'account': DefinitionsAccount, 'is_sticky': {'type': 'boolean'}, 'is_hidden': {'type': 'boolean'}, 'review_status': {'type': 'string'}, 'id': {'type': 'string'}}}
DefinitionsArticle = {'properties': {'status': {'type': 'string'}, 'account': DefinitionsAccount, 'voice': DefinitionsVoicelite, 'title': {'type': 'string'}, 'column_id': {'type': 'string'}, 'content': {'type': 'string'}, 'date_published': DefinitionsDatetime, 'date_created': DefinitionsDatetime, 'is_hidden': {'type': 'boolean'}, 'summary': {'type': 'string'}, 'id': {'type': 'string'}}}
DefinitionsPost = {'properties': {'account': DefinitionsAccount, 'description': {'type': 'string'}, 'is_sticky': {'type': 'boolean'}, 'title': {'type': 'string'}, 'review_status': {'type': 'string'}, 'date_published': DefinitionsDatetime, 'is_hidden': {'type': 'boolean'}, 'id': {'type': 'string'}}}
DefinitionsPostlite = {'properties': {'account': DefinitionsAccount, 'description': {'type': 'string'}, 'is_sticky': {'type': 'boolean'}, 'title': {'type': 'string'}, 'review_status': {'type': 'string'}, 'date_published': DefinitionsDatetime, 'is_hidden': {'type': 'boolean'}, 'id': {'type': 'string'}}}
DefinitionsColumnlite = {'properties': {'status': {'type': 'string'}, 'account': DefinitionsAccount, 'name': {'type': 'string'}, 'date_created': DefinitionsDatetime, 'price': {'type': 'integer'}, 'subscribes_count': {'type': 'integer', 'format': 'int32'}, 'id': {'type': 'string'}}}
DefinitionsUpdatecolumn = {'properties': {'status': {'enum': ['draft', 'published'], 'type': 'string'}, 'name': {'type': 'string'}, 'image': {'type': 'string'}, 'date_start': DefinitionsDatetime, 'content': {'type': 'string'}, 'is_hidden': {'type': 'boolean'}, 'price': {'type': 'integer'}, 'date_end': DefinitionsDatetime}}
DefinitionsColumn = {'properties': {'status': {'type': 'string'}, 'account': DefinitionsAccount, 'views_count': {'type': 'integer', 'format': 'int32'}, 'price': {'type': 'integer'}, 'date_start': DefinitionsDatetime, 'id': {'type': 'string'}, 'content': {'type': 'string'}, 'date_created': DefinitionsDatetime, 'is_hidden': {'type': 'boolean'}, 'voice': DefinitionsVoice, 'date_end': DefinitionsDatetime, 'name': {'type': 'string'}}}
DefinitionsReplylite = {'properties': {'content': {'type': 'string'}, 'date_published': DefinitionsDatetime, 'account': DefinitionsAccount, 'is_sticky': {'type': 'boolean'}, 'is_hidden': {'type': 'boolean'}, 'review_status': {'type': 'string'}, 'id': {'type': 'string'}}}

validators = {
    ('columns_id_posts', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'account_id': {'description': 'account id in query', 'format': 'int32', 'required': False, 'type': 'integer'}, 'is_sticky': {'required': False, 'type': 'boolean', 'description': 'is_sticky in query'}, 'review_status': {'required': False, 'description': 'review_status in query', 'enum': ['pending', 'passwd', 'rejected', 'auto_passed'], 'type': 'string'}, 'post_id': {'required': False, 'type': 'string', 'description': 'post id in query'}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 20000}, 'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'is_hidden': {'required': False, 'type': 'boolean', 'description': 'is_hidden in query'}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 1000}}}},
    ('posts_id_replies', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'account_id': {'description': 'account id in query', 'format': 'int32', 'required': False, 'type': 'integer'}, 'is_sticky': {'required': False, 'type': 'boolean', 'description': 'is_sticky in query'}, 'review_status': {'required': False, 'description': 'review_status in query', 'enum': ['pending', 'passwd', 'rejected', 'auto_passed'], 'type': 'string'}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'reply_id': {'required': False, 'type': 'string', 'description': 'reply id in query'}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 20000}, 'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'is_hidden': {'required': False, 'type': 'boolean', 'description': 'is_hidden in query'}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 1000}}}},
    ('replies', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatereply},
    ('replies', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'account_id': {'description': 'account id in query', 'format': 'int32', 'required': False, 'type': 'integer'}, 'is_sticky': {'required': False, 'type': 'boolean', 'description': 'is_sticky in query'}, 'review_status': {'required': False, 'description': 'review_status in query', 'enum': ['pending', 'passwd', 'rejected', 'auto_passed'], 'type': 'string'}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'column_id': {'required': False, 'type': 'string', 'description': u'\u4e13\u680fID'}, 'post_id': {'required': False, 'type': 'string', 'description': 'post id in query'}, 'reply_id': {'required': False, 'type': 'string', 'description': 'reply id in query'}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 20000}, 'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'is_hidden': {'required': False, 'type': 'boolean', 'description': 'is_hidden in query'}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 1000}}}},
    ('articles_id_publish', 'PUT'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('articles_id_publish', 'DELETE'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('replies_id', 'PUT'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsUpdatereply},
    ('replies_id', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('articles', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatearticle},
    ('articles', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'status': {'required': False, 'description': 'status in query', 'enum': ['draft', 'published'], 'type': 'string'}, 'account_id': {'description': 'account id in query', 'format': 'int32', 'required': False, 'type': 'integer'}, 'column_id': {'required': False, 'type': 'string', 'description': u'\u4e13\u680fID'}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 20000}, 'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'is_hidden': {'required': False, 'type': 'boolean', 'description': 'is_hidden in query'}, 'article_id': {'required': False, 'type': 'string', 'description': u'\u6587\u7ae0ID'}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 1000}}}},
    ('articles_id', 'PUT'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsUpdatearticle},
    ('articles_id', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('posts_id_review', 'PUT'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsUpdatepost},
    ('columns_id', 'PUT'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsUpdatecolumn},
    ('columns_id', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('columns', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatecolumn},
    ('columns', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'status': {'required': False, 'description': 'status in query', 'enum': ['draft', 'published'], 'type': 'string'}, 'account_id': {'description': 'account id in query', 'format': 'int32', 'required': False, 'type': 'integer'}, 'column_id': {'required': False, 'type': 'string', 'description': u'\u4e13\u680fID'}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 20000}, 'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'is_hidden': {'required': False, 'type': 'boolean', 'description': 'is_hidden in query'}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 1000}}}},
    ('posts_id', 'PUT'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsUpdatepost},
    ('posts_id', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('columns_id_publish', 'PUT'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('columns_id_publish', 'DELETE'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}},
    ('posts', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatepost},
    ('posts', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'account_id': {'description': 'account id in query', 'format': 'int32', 'required': False, 'type': 'integer'}, 'is_sticky': {'required': False, 'type': 'boolean', 'description': 'is_sticky in query'}, 'review_status': {'required': False, 'description': 'review_status in query', 'enum': ['pending', 'passwd', 'rejected', 'auto_passed'], 'type': 'string'}, 'column_id': {'required': False, 'type': 'string', 'description': u'\u4e13\u680fID'}, 'limit': {'description': 'limit number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'offset': {'description': 'offset number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 20000}, 'per_page': {'description': 'per_page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 100}, 'is_hidden': {'required': False, 'type': 'boolean', 'description': 'is_hidden in query'}, 'page': {'description': 'page number', 'format': 'int32', 'required': False, 'type': 'integer', 'maximum': 1000}}}},
    ('replies_id_review', 'PUT'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsUpdatereply},
    ('voices', 'POST'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'json': DefinitionsCreatevoice},
    ('voices', 'GET'): {'headers': {'required': ['Authorization'], 'properties': {'Authorization': {'type': 'string'}}}, 'args': {'required': [], 'properties': {'article_id': {'required': False, 'type': 'string', 'description': u'\u6587\u7ae0ID'}}}},
}

filters = {
    ('columns_id_posts', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsPostlite, 'type': 'array'}}},
    ('posts_id_replies', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsReplylite, 'type': 'array'}}},
    ('replies', 'POST'): {201: {'headers': None, 'schema': DefinitionsReply}},
    ('replies', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsReplylite, 'type': 'array'}}},
    ('articles_id_publish', 'PUT'): {200: {'headers': None, 'schema': DefinitionsArticle}},
    ('articles_id_publish', 'DELETE'): {204: {'headers': None, 'schema': DefinitionsNone}},
    ('replies_id', 'PUT'): {200: {'headers': None, 'schema': DefinitionsReply}},
    ('replies_id', 'GET'): {200: {'headers': None, 'schema': DefinitionsReply}},
    ('articles', 'POST'): {201: {'headers': None, 'schema': DefinitionsArticle}},
    ('articles', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsArticlelite, 'type': 'array'}}},
    ('articles_id', 'PUT'): {200: {'headers': None, 'schema': DefinitionsArticle}},
    ('articles_id', 'GET'): {200: {'headers': None, 'schema': DefinitionsArticle}},
    ('posts_id_review', 'PUT'): {200: {'headers': None, 'schema': DefinitionsSuccess}},
    ('columns_id', 'PUT'): {200: {'headers': None, 'schema': DefinitionsColumn}},
    ('columns_id', 'GET'): {200: {'headers': None, 'schema': DefinitionsColumn}},
    ('columns', 'POST'): {201: {'headers': None, 'schema': DefinitionsColumn}},
    ('columns', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsColumnlite, 'type': 'array'}}},
    ('posts_id', 'PUT'): {200: {'headers': None, 'schema': DefinitionsPost}},
    ('posts_id', 'GET'): {200: {'headers': None, 'schema': DefinitionsPost}},
    ('columns_id_publish', 'PUT'): {200: {'headers': None, 'schema': DefinitionsColumn}},
    ('columns_id_publish', 'DELETE'): {204: {'headers': None, 'schema': DefinitionsNone}},
    ('posts', 'POST'): {201: {'headers': None, 'schema': DefinitionsPost}},
    ('posts', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsPostlite, 'type': 'array'}}},
    ('replies_id_review', 'PUT'): {200: {'headers': None, 'schema': DefinitionsSuccess}},
    ('voices', 'POST'): {201: {'headers': None, 'schema': DefinitionsVoice}},
    ('voices', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsVoice, 'type': 'array'}}},
}

scopes = {
    ('columns_id_posts', 'GET'): ['panel'],
    ('posts_id_replies', 'GET'): ['panel'],
    ('replies', 'POST'): ['panel'],
    ('replies', 'GET'): ['panel'],
    ('articles_id_publish', 'PUT'): ['panel'],
    ('articles_id_publish', 'DELETE'): ['panel'],
    ('replies_id', 'PUT'): ['panel'],
    ('replies_id', 'GET'): ['panel'],
    ('articles', 'POST'): ['panel'],
    ('articles', 'GET'): ['panel'],
    ('articles_id', 'PUT'): ['panel'],
    ('articles_id', 'GET'): ['panel'],
    ('posts_id_review', 'PUT'): ['panel'],
    ('columns_id', 'PUT'): ['panel'],
    ('columns_id', 'GET'): ['panel'],
    ('columns', 'POST'): ['panel'],
    ('columns', 'GET'): ['panel'],
    ('posts_id', 'PUT'): ['panel'],
    ('posts_id', 'GET'): ['panel'],
    ('columns_id_publish', 'PUT'): ['panel'],
    ('columns_id_publish', 'DELETE'): ['panel'],
    ('posts', 'POST'): ['panel'],
    ('posts', 'GET'): ['panel'],
    ('replies_id_review', 'PUT'): ['panel'],
    ('voices', 'POST'): ['panel'],
    ('voices', 'GET'): ['panel'],
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

