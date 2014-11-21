from os.path import join
import os
import unittest

from continuum_flask import server
import flask
import mock

# Configuration for Flask
# TODO: Refactor so Flask takes a dict
ROOT_PATH = os.getcwd()


class FlaskTestCase(unittest.TestCase):
    def generate_server(self):
        return server.Flask('generated_server', settings=__name__)

    def test_is_subclass_of_flask(self):
        f = self.generate_server()
        self.assertIsInstance(f, flask.Flask)

    def test_sets_static_url_path_by_default(self):
        f = self.generate_server()
        self.assertEqual('/static', f.static_url_path)

    def test_sets_static_folder_based_on_root_path(self):
        f = self.generate_server()
        self.assertEqual(join(ROOT_PATH, 'build'), f.static_folder)

    def test_defers_to_static_folder_if_present(self):
        f = server.Flask('foo', settings=__name__, static_folder='foo')
        self.assertEqual(join(os.getcwd(), 'foo'), f.static_folder)

    def test_does_not_change_static_url_path_if_static_folder_present(self):
        f = server.Flask('foo', settings=__name__, static_folder='foo')
        self.assertEqual('/foo', f.static_url_path)

    def test_static_available_in_context(self):
        f = self.generate_server()
        with f.test_request_context():
            template = 'URL: {{ static("foo") }}'
            result = flask.render_template_string(template)
            self.assertEqual('URL: /static/foo', result)

    def test_allows_dict_to_provide_settings(self):
        f = server.Flask('foo', settings={'ROOT_PATH': 'foo'})
        self.assertEqual(join(os.getcwd(), 'foo', 'build'), f.static_folder)

    def test_dispatches_to_helpers_setup_blueprint(self):
        with mock.patch.object(server, 'helpers') as helpers:
            f = server.Flask('foo')
        helpers.setup_blueprints.assert_called_with(f, None)

    def test_provides_blueprints_to_setup_blueprints(self):
        blueprints = [mock.Mock(), mock.Mock()]
        with mock.patch.object(server, 'helpers') as helpers:
            f = server.Flask('foo', blueprints=blueprints)
        helpers.setup_blueprints.assert_called_with(f, blueprints)

    def test_defaults_root_path_to_cwd(self):
        f = server.Flask('foo', settings={})
        self.assertEqual(join(os.getcwd(), 'build'), f.static_folder)
