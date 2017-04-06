# -*- coding: utf-8 -*-

from flask import g


class CacheMeta(object):

    meta_name = None
    meta_ids = None

    def __init__(self, ids=None, obj_type='int', field_name='id',
                 is_refresh=False):
        """
        将指定用户预加载到 model_meta 缓存

        支持三种形式 ids 传递

        a. plain int: [12345678, 387474983, ...]
        b. plain string: ['12345678', '387474983', ...]
        c. object attr: [object(id=283749479), object(order_id='9437845937'), .]
        d. dict key: [{'id': 1893873494}, {'id': 9374923792}, ...]

        :Parameters
            - ids model id 列表或者含有id 的对象列表
            - field_name 含有id 的对象/字典中，id 对应的字段名
        """

        self.ids = ids
        self.field_name = field_name
        self.is_refresh = is_refresh

    def preload_meta(self):
        if self.ids is None:
            self.ids = []

        meta_ids = getattr(g, self.meta_ids, [])
        if meta_ids:
            self.ids = self.ids + list(meta_ids)
        ids_set = set([])
        for id in self.ids:
            if id is None:
                continue
            if isinstance(id, (int, str, unicode)):
                ids_set.add(id)
            else:
                try:
                    ids_set.add(getattr(id, self.field_name))
                except AttributeError:
                    ids_set.add(id[self.field_name])

        if not ids_set:
            return ''

        try:
            metas = self._get_metadata(*ids_set)
        except:
            raise
        else:
            setattr(g, self.meta_ids, set([]))

        try:
            _metas = getattr(g, self.meta_name, {})
            _metas.update(metas)
            setattr(g, self.meta_name, _metas)
        except AttributeError:
            setattr(g, self.meta_name, metas)
        return ''

    def _meta_values(self, id):
        if (not hasattr(g, self.meta_name) or
                id not in getattr(g, self.meta_name)):
            self.preload_meta()

        try:
            return getattr(g, self.meta_name)[id]
        except (TypeError, KeyError, AttributeError):
            return {}

    @classmethod
    def preload_meta_datas(cls, ids=None, field_name='id'):
        obj_meta = cls(ids, field_name=field_name)
        obj_meta.preload_meta()
        return getattr(g, obj_meta.meta_name, {})

    @classmethod
    def get_meta_by_id(cls, obj_id, is_refresh=False, **kwargs):
        pass

    @classmethod
    def refresh_meta(cls, obj_id):
        return cls.get_meta_by_id(obj_id, is_refresh=True)
