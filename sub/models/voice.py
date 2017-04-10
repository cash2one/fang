# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werkzeug.utils import cached_property

from zaih_core.database import (
    db, Model, DateTime, generator_string_id)


__all__ = [
    'Voice',
]


def voice_id_generator():
    return generator_string_id(18, 3)


class Voice(Model):

    __tablename__ = 'voice'

    STATUS_DRAFT = 'draft'
    STATUS_SUCCEED = 'succeed'

    SOURCE_WEIXIN = 'weixin'
    SOURCE_QINIU = 'qiniu'

    TARGET_TYPE_ARTICLE = 'article'

    REVIEW_STATUS_AUTO_PASSED = 'auto_passed'  # 审核通过
    REVIEW_STATUS_REJECTED = 'rejected'        # 审核未通过
    REVIEW_STATUS_PENDING = 'pending'          # 待审核
    REVIEW_STATUS_PASSED = 'passed'            # 审核通过

    PUBLIC_REVIEW_STATUSES = [REVIEW_STATUS_PASSED, REVIEW_STATUS_AUTO_PASSED]

    id = db.Column(
        db.String(32), primary_key=True, default=voice_id_generator)
    media_id = db.Column(db.String(), nullable=False)
    voice_key = db.Column(db.String(), nullable=True)
    duration = db.Column(db.Integer(), nullable=False)
    target_id = db.Column(db.String(32), nullable=False, index=True)
    target_type = db.Column(
        db.String(16), nullable=False, index=True, server_default=TARGET_TYPE_ARTICLE)
    source = db.Column(
        db.String(), nullable=True, index=True, default=SOURCE_WEIXIN)
    status = db.Column(
        db.String(), nullable=False, index=True, server_default=STATUS_DRAFT)
    review_status = db.Column(
        db.String(32), nullable=False,
        server_default=REVIEW_STATUS_PENDING, index=True)
    date_created = db.Column(
        db.DateTime(timezone=True), nullable=False, index=True,
        server_default=db.func.current_timestamp())
    date_updated = db.Column(
        DateTime, nullable=False, index=True,
        server_default=db.func.current_timestamp())

    article = db.relationship(
        'Article',
        backref=db.backref('_voice', lazy='joined', uselist=False),
        primaryjoin='and_(Article.id==Voice.target_id, Voice.target_type=="article")',
        foreign_keys='Voice.target_id',
        uselist=False)

    @cached_property
    def _voice(self):
        from sub.services.media import (
            get_weixin_media_url, qiniu_sign_url)
        if (self.status == self.STATUS_DRAFT and
                self.source == self.SOURCE_WEIXIN):
            return get_weixin_media_url(self.media_id)
        else:
            return qiniu_sign_url(self.voice_key)

    @cached_property
    def voice_url(self):
        return self._voice

    @cached_property
    def url(self):
        return self._voice
