# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import g

from sub.models import Reply
from sub.app import redis


def get_post_replies_count(post_id):
    count = (
        Reply.query
        .filter(~Reply.is_hidden)
        .filter(Reply.post_id == post_id)
        .filter(Reply.review_status.in_(Reply.PUBLIC_REVIEW_STATUSES))
        .count())
    return count


class PostStatistics(object):

    def __init__(self, id, single=False):
        self.id = id
        self.single = single
        self.skey = 'post:%s:statistics' % id

    def init(self):
        statistics = {
            'replies_count': get_post_replies_count(self.id),
        }
        return statistics

    def update_replies_count(self):
        count = get_post_replies_count(self.id)
        self.update('replies_count', count)

    def update(self, init=False, **kwargs):
        '''
        :params replies_count              讨论回复数
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
    def replies_count(self):
        key = 'replies_count'
        return self._get_count(key)
