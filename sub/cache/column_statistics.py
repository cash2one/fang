# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import g

from sub.models import Member
from sub.app import redis


def get_members_count(column_id):
    count = (
        Member.query
        .filter(Member.column_id == column_id)
        .count())
    return count


class ColumnStatistics(object):

    def __init__(self, id, single=False):
        self.id = id
        self.single = single
        self.skey = 'column:%s:statistics' % id

    def init(self):
        statistics = {
            'members_count': get_members_count(self.id),
        }
        return statistics

    def update_members_count(self, count=None):
        key = 'members_count'
        if not count:
            count = get_members_count(self.id)
        self.update(key, count)

    def update(self, init=False, **kwargs):
        '''
        :params members_count              订阅数
        '''
        if init:
            statistics = self.init()
            redis.hmset(self.skey, statistics)
        else:
            redis.hmset(self.skey, kwargs)

    def get_all(self):
        statistics = getattr(g, self.skey, None)
        if statistics is None:
            statistics = redis.hgetall(self.skey)
            setattr(g, self.skey, statistics)
        return statistics

    def get_single(self, key):
        statistics = self.get_all()
        count = statistics.get(key)
        return int(count or 0)

    def _get_count(self, key):
        if self.single:
            return self.get_single(key)
        statistics = self.get_all()
        return int(statistics.get(key, 0))

    @property
    def members_count(self):
        key = 'members_count'
        return self._get_count(key)
