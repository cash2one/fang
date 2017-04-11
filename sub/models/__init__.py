from .column import *  # noqa
from .post import *  # noqa
from .action import *  # noqa
from .active import *  # noqa
from .article import *  # noqa
from .voice import *  # noqa
from .order import *  # noqa


from flask import g
import flask_sqlalchemy as fsa
from sqlalchemy.orm.attributes import get_history


def get_added_and_deleted(model, field):
    # get field history value and current value
    key = 'model_{name}:{id}:old_{field}'.format(name=model.__tablename__,
                                                 id=model.id,
                                                 field=field)
    old_value = getattr(g, key, None)
    added, unchanged, deleted = get_history(model, field)
    new_value = unchanged[0]
    return old_value, new_value


def on_models_committed(sender, changes):
    from sub.tasks import process_after_liking
    for model, change in changes:
        if isinstance(model, Liking) and change == 'insert':
            process_after_liking.delay(voice_id=model.id)
        elif isinstance(model, Reply) and change == 'insert':
            process_after_reply.delay(model.id)


def before_models_committed(sender, changes):
    for model, change in changes:
        if isinstance(model, Voice) and change == 'update':
            added, unchanged, deleted = get_history(model, 'status')
            if deleted:
                old_status = deleted[0]
                setattr(g, 'voice_%s_old_status' % model.id, old_status)


fsa.models_committed.connect(on_models_committed)
fsa.before_models_committed.connect(before_models_committed)
