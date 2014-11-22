from __future__ import absolute_import

from flask import url_for
from werkzeug.utils import import_string


class AttributeDict(dict):
    def __getattr__(self, *args):
        try:
            return self.__getitem__(*args)
        except KeyError:
            raise AttributeError(*args)

    def __setattr__(self, *args):
        try:
            return self.__setitem__(*args)
        except KeyError:
            raise AttributeError(*args)


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
            if type(b) is str:
                app.register_blueprint(import_string(b).blueprint)
            elif len(b) == 1:
                app.register_blueprint(import_string(b[0]).blueprint)
            elif len(b) == 3:
                app.register_blueprint(import_string(b[0]).blueprint,
                                       *b[1], **b[2])
            else:
                kwargs = {}
                args = b[1]
                if type(args) is dict:
                    kwargs = args
                    args = ()
                app.register_blueprint(import_string(b[0]).blueprint,
                                       *args, **kwargs)
