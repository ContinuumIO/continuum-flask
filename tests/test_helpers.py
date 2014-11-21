import os
import random
import unittest

from continuum_flask import Flask
from continuum_flask import helpers

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
