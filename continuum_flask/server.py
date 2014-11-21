from __future__ import absolute_import
import os
from os.path import join

import flask

from . import helpers


class Flask(flask.Flask):
    def __init__(self, name, settings=None, *args, **kwargs):
        settings = helpers.import_settings(name, settings_module=settings)
        if not 'static_folder' in kwargs:
            ROOT_PATH = getattr(settings, 'ROOT_PATH', os.getcwd())
            kwargs.update({
                'static_folder': join(ROOT_PATH, 'build'),
                'static_url_path': '/static',
            })
        blueprints = kwargs.pop('blueprints', None)
        super(Flask, self).__init__(name, *args, **kwargs)
        self.setup_jinja_context_variables()

        helpers.setup_blueprints(self, blueprints)

    def setup_jinja_context_variables(self):
        self.jinja_env.globals.update({
            'static': helpers.static_helper
        })
