from __future__ import absolute_import

from flask import url_for
from werkzeug.utils import import_string


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def static_helper(filename):
    # TODO support CDNs
    return url_for('static', filename=filename)


def import_settings(name, settings_module=None):
    if type(settings_module) is dict:
        return AttributeDict(**settings_module)

    if settings_module is None:
        settings_module = '{}.{}'.format(name, 'settings')
    return import_string(settings_module)


def setup_blueprints(app, blueprints=None):
    if blueprints is None:
        return

    with app.app_context():
        for b in blueprints:
            app.register_blueprint(import_string(b).blueprint)
