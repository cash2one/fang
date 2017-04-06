# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask

import panel


def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        panel.bp,
        url_prefix='/panel')
    return app

if __name__ == '__main__':
    create_app().run(debug=True)