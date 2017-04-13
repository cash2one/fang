# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from flask import g

from zaih_core.ztime import now

from sub.models import Liking
from sub.app import redis


def get_reply_likings_count(reply_id):
    count = (
        Liking.query
        .filter(Liking.target_id == reply_id)
        .filter(Liking.target_type == Liking.TARGET_TYPE_REPLY)
        .count())
    return count


class ReplyStatistics(object):

    def __init__(self, id, single=False):
        self.id = id
        self.single = single
        self.skey = 'reply:%s:statistics' % id
        self.likings_key = 'reply:%s:likings' % id

    def init(self):
        statistics = {
            'likings_count': get_reply_likings_count(self.id),
        }
        return statistics

    def update_likings_count(self, count=None):
        key = 'likings_count'
        if not count:
            count = get_reply_likings_count(self.id)
        self.update(key, count)

    def update_likings(self, account_id, is_delete=False, score=None):
        if score is None:
            score = time.mktime(now().timetuple())
        if is_delete:
            redis.zrem(self.likings_key, account_id)
        else:
            redis.zadd(self.likings_key, score, account_id)
        count = redis.zcard(self.likings_key)
        self.update_likings_count(count=count)

    def update(self, init=False, **kwargs):
        '''
        :params likings_count              讨论回复点赞数
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
    def likings_count(self):
        key = 'likings_count'
        return self._get_count(key)

    def has_liked(self, account_id):
        score = redis.zscore(self.likings_key, account_id)
        return True if score else False
