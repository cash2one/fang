# -*- coding: utf-8 -*-
from flask import g
from . import Resource

from zaih_core.api_errors import NotFound

from sub.models import Reply
from sub.services.permissions import register_permission
from zaih_core.api_errors import NotFound, BadRequest


class RepliesIdReview(Resource):
    
    # @register_permission('update_reply')
    def put(self, id):
        review_action = g.json.get('review_action')
        reply = Reply.query.get(id)
        
        if not reply:
            raise NotFound('reply_not_found')
        if reply.review_status not in [
                Reply.REVIEW_STATUS_PENDING,
                Reply.REVIEW_STATUS_AUTO_PASSED]:
            raise BadRequest('reply_review_status_error')
        
        reply.update(review_status=review_action)
        return {'ok': True}, 200