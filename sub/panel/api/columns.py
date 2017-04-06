# -*- coding: utf-8 -*-
from flask import g

from . import Resource


class Columns(Resource):

    def get(self):
        filter_fields = ['id', 'is_digest', 'is_pro',
                         'is_hidden', 'status', 'account_id', 'review_status']
        query = get_slave_query(Recourse, filter_fields, g.args)

        is_replied = g.args.get('is_replied')
        if is_replied is True:
            query = (
                query
                .filter(Recourse.date_last_reply != Recourse.date_created))
        elif is_replied is False:
            query = (
                query
                .filter(Recourse.date_last_reply == Recourse.date_created))

        tag_id = g.args.get('tag_id')
        if tag_id:
            query = (
                query
                .filter(Recourse.id == RecourseTag.recourse_id)
                .filter(RecourseTag.tag_id == tag_id))
        elif tag_id == '':
            query = (
                query
                .filter(~db.exists().where(
                    RecourseTag.recourse_id == Recourse.id)))

        is_with_image = g.args.get('is_with_image')
        if is_with_image is not None:
            if is_with_image:
                query = (
                    query
                    .filter(Recourse.id == Image.target_id)
                    .filter(Image.target_type == "recourse"))
            else:
                query = (
                    query
                    .filter(~db.exists().where(
                        Recourse.id == Image.target_id)))

        order_by = g.args.get('order_by', 'date_created')
        if order_by == 'date_last_reply':
            query = (
                query
                .filter(Recourse.date_last_reply != Recourse.date_created))
        count = query.count()

        offset, limit = get_offset_limit(g.args)
        order_dict = {
            'date_created': Recourse.date_created.desc(),
            'date_last_reply': Recourse.date_last_reply.desc(),
            'order_score': Recourse.order_score.desc(),
            'score': Recourse.score.desc(),
        }
        order_by = order_dict.get(order_by)
        recourses = (query
                     .order_by(order_by)
                     .offset(offset).limit(limit)
                     .all())
        return recourses, 200, [('Total-Count', str(count))]

    @register_permission('create_recourse')
    def post(self):
        # 后台添加一条悬赏 只能添加高额悬赏
        # 添加成功后 需要在pay中添加一条数据
        is_pro = g.json['is_pro']
        if not is_pro:
            raise BadRequest('recourse_pro_only')
        g.json.update({
            'status': Recourse.STATUS_PAID,
            'review_status': Recourse.REVIEW_STATUS_PASSED
        })
        g.json['operator_id'] = g.account.id
        pro_attrs = ['accept_mode', 'introduction', 'accept_description',
                     'max_accept_count', 'date_finished', 'image',
                     'introduction_type']
        pro_data = {}
        for attr in pro_attrs:
            value = g.json.pop(attr, None)
            if value:
                if attr == 'date_finished':
                    value = str_to_time(value)
                pro_data[attr] = value
        recourse = Recourse.create(**g.json)
        pro_data['recourse_id'] = recourse.id
        RecoursePro.create(**pro_data)
        return recourse
