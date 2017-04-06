# -*- coding: utf-8 -*-

def filter_params(filter_fields, params):
    new_params = {k: v for k, v in params.items() if k in filter_fields}
    return new_params


def get_query(model, filter_fields, params):
    new_params = filter_params(filter_fields, params)
    return model.query.filter_by(**new_params)


def make_template_data(openid, template_id, url, **kwargs):
    message = {
        "touser": openid,
        "template_id": template_id,
        "url": url,
    }
    data = {}
    for k, v in kwargs.items():
        data[k] = {
            "value": v,
            "color": "#173177"
        }
    message["data"] = data
    return message



