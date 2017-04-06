# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from flask import Blueprint, views, request
from requests.exceptions import ConnectTimeout, ReadTimeout

from sub.models import Voice
from sub.utils import error_notice
from sub.services.media import (
    qiniu_private_avinfo_duration, media_fetch)

blueprint = Blueprint('media', __name__, url_prefix='/py')


class QiniuPfopNotify(views.MethodView):

    def post(self):
        # 录音多媒体处理通知 修改voices
        notify_info = json.loads(request.data)
        code = notify_info.get('code')
        if code == 0:
            items = notify_info.get('items')
            if items:
                key = items[0].get('key')
                voice = Voice.query.filter(Voice.voice_key == key).first()
                if not voice:
                    return 'fail'
                if Voice.status == Voice.STATUS_SUCCEED:
                    return 'success'
                try:
                    duration = qiniu_private_avinfo_duration(voice.voice_key)
                except (ConnectTimeout, ReadTimeout):
                    # 超时重试
                    if voice.source == Voice.SOURCE_WEIXIN:
                        media_fetch(voice.media_id)
                    return 'fail'
                if duration:
                    voice.update(duration=duration,
                                 status=Voice.STATUS_SUCCEED)
                else:
                    error_notice('答案语音错误: %s' % voice.id,
                                 kw1='答案语音地址不对')
                    return 'fail'
        return 'success'


blueprint.add_url_rule('/qiniu/pfop/notify', endpoint='pfop_notify',
                       view_func=QiniuPfopNotify.as_view(b'pfop_notify'))
