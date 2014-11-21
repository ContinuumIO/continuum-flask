import os
import random
import unittest

from continuum_flask import Flask
from continuum_flask import helpers
import mock

TESTING = True
ROOT_PATH = os.getcwd()


class static_helper_test(unittest.TestCase):
    def setUp(self):
        f = self.f = Flask(__name__, settings=__name__)
        f.config['TESTING'] = True

    def test_returns_url_for_given_static_resource(self):
        r = random.randint(1000, 2000)
        with self.f.test_request_context('/'):
            for s in ['foo', 'bar', 'random-%s' % r]:
                self.assertEqual(
                    '/static/%s' % s,
                    helpers.static_helper(s),
                    msg="generating static url for [%s]" % s)


class import_settings_test(unittest.TestCase):
    def test_imports_module_if_string_provided(self):
        m = helpers.import_settings('foo', settings_module=__name__)
        self.assertEqual(m.__name__, self.__module__)

    def test_defaults_to_name_dot_settings(self):
        with mock.patch.object(helpers, 'import_string') as stub:
            helpers.import_settings('foo')
        stub.assert_called_with('foo.settings')

    def test_uses_settings_module_if_present(self):
        with mock.patch.object(helpers, 'import_string') as stub:
            helpers.import_settings('foo', 'bar.settings')
        stub.assert_called_with('bar.settings')
