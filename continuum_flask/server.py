from __future__ import absolute_import
from os.path import join

import flask
from werkzeug.utils import import_string

from . import helpers


class Flask(flask.Flask):
    def __init__(self, name, settings=None, *args, **kwargs):
        settings = helpers.import_settings(name, settings_module=settings)
        if not 'static_folder' in kwargs:
            kwargs.update({
                'static_folder': join(settings.ROOT_PATH, 'build'),
                'static_url_path': '/static',
            })
        blueprints = kwargs.pop('blueprints', None)
        super(Flask, self).__init__(name, *args, **kwargs)
        self.setup_jinja_context_variables()

        self.setup_blueprints(blueprints)

    def setup_blueprints(self, blueprints):
        if blueprints is None:
            return
        with self.app_context():
            for b in blueprints:
                self.register_blueprint(import_string(b).blueprint)

    def setup_jinja_context_variables(self):
        self.jinja_env.globals.update({
            'static': helpers.static_helper
        })
