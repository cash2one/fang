# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from zaih_core.ztime import now

from sub.app import redis
from sub.models import Member


class ColumnMembers(object):

    def __init__(self, id):
        self.column_id = id
        self.mkey = 'column:%s:members' % id

    def count(self):
        count = redis.zcount(self.mkey, '-inf', '+inf')
        return count or 0

    def update_members(self, account_id, is_deleted=False):
        if is_deleted:
            redis.zrem(self.mkey, account_id)
        else:
            score = time.mktime(now().timetuple())
            redis.zadd(self.mkey, score, account_id)

    def is_subscribed(self, account_id):
        return redis.sismember(self.mkey, account_id)

    def full_sync(self):
        # 全量更新缓存
        members = Member.query.filter_by(column_id=self.id).all()
        for member in members:
            score = time.mktime(member.date_created.timetuple())
            redis.zadd(self.mkey, score, member.account_id)
