import os
import random
import unittest

from continuum_flask import helpers, server
import mock

TESTING = True
ROOT_PATH = os.getcwd()

stub_blueprint = lambda b: mock.Mock(blueprint=b)


class AttributeDictTestCase(unittest.TestCase):
    def test_allows_accessing_dict_as_obj(self):
        d = helpers.AttributeDict(foo='bar', bar='foo')
        self.assertEqual(d.foo, 'bar')
        self.assertEqual(d.bar, 'foo')
        self.assertEqual(d.foo, d['foo'])
        self.assertEqual(d.bar, d['bar'])

    def test_allows_getattr_to_be_used_to_set_default(self):
        d = helpers.AttributeDict(foo='bar')
        self.assertTrue(getattr(d, 'unknown', True))
        self.assertFalse(getattr(d, 'unknowable', False))

    def test_allows_setting(self):
        d = helpers.AttributeDict(foo='bar')
        d['foo'] = 'baz'
        self.assertEqual(d.foo, 'baz')

        d.foo = 'biz'
        self.assertEqual(d.foo, 'biz')


class static_helper_test(unittest.TestCase):
    def setUp(self):
        f = self.f = server.Flask(__name__, settings=__name__)
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


class setup_blueprints_test(unittest.TestCase):
    def generate_server(self):
        return server.Flask('generated_server', settings=__name__)

    def generate_app(self):
        register_blueprint = mock.Mock()
        app_context = mock.Mock()
        app_context.return_value = app_context
        app_context.__enter__ = mock.Mock()
        app_context.__exit__ = mock.Mock()
        app = mock.Mock(
            register_blueprint=register_blueprint,
            app_context=app_context,
        )
        return app

    def generate_blueprints(self):
        b1 = mock.Mock(blueprint='blueprint 1')
        b2 = mock.Mock(blueprint='blueprint 2')
        return b1, b2

    def test_does_nothing_with_no_blueprints(self):
        helpers.setup_blueprints(self.generate_server(), None)

    def test_imports_each_blueprint(self):
        b1, b2 = self.generate_blueprints()
        app = self.generate_app()

        with mock.patch.object(helpers, 'import_string') as import_string:
            import_string.side_effect = [b1, b2]
            helpers.setup_blueprints(app, ['blueprint.one', 'blueprint.two'])

        import_string.assert_has_calls([
            mock.call('blueprint.one'),
            mock.call('blueprint.two'),
        ])

    def test_register_each_blueprint(self):
        b1, b2 = self.generate_blueprints()
        app = self.generate_app()

        with mock.patch.object(helpers, 'import_string') as import_string:
            import_string.side_effect = [b1, b2]
            helpers.setup_blueprints(app, ['foo', 'bar'])

        self.assert_(app.register_blueprint.called, msg='sanity check')
        self.assertEqual(2, app.register_blueprint.call_count)
        app.register_blueprint.assert_has_calls([
            mock.call(b1.blueprint),
            mock.call(b2.blueprint),
        ])

    def test_is_called_with_app_context(self):
        app = self.generate_app()

        with mock.patch.object(helpers, 'import_string') as import_string:
            import_string.side_effect = self.generate_blueprints()
            helpers.setup_blueprints(app, ['foo', 'bar'])

        self.assertEqual(1, app.app_context.call_count)

    def test_adds_args_and_kwargs_if_not_simple_string(self):
        app = self.generate_app()
        with mock.patch.object(helpers, 'import_string') as import_string:
            import_string.side_effect = [stub_blueprint('foo'), ]
            blueprints = [
                ['foo', ('arg1', 'arg2'), {'kwarg1': 'foo', 'kwarg2': 'bar'}],
            ]
            helpers.setup_blueprints(app, blueprints=blueprints)

        app.register_blueprint.assert_has_calls([
            mock.call('foo', 'arg1', 'arg2', kwarg1='foo', kwarg2='bar')
        ])

    def test_can_handle_kwargs_only(self):
        app = self.generate_app()
        with mock.patch.object(helpers, 'import_string') as import_string:
            import_string.side_effect = [stub_blueprint('foo'), ]
            blueprints = [
                ['foo', {'kwarg1': 'foo', 'kwarg2': 'bar'}],
            ]
            helpers.setup_blueprints(app, blueprints=blueprints)

        app.register_blueprint.assert_has_calls([
            mock.call('foo', kwarg1='foo', kwarg2='bar')
        ])

    def test_can_handle_args_only(self):
        app = self.generate_app()
        with mock.patch.object(helpers, 'import_string') as import_string:
            import_string.side_effect = [stub_blueprint('foo'), ]
            blueprints = [
                ['foo', ('arg1', 'arg2')]
            ]
            helpers.setup_blueprints(app, blueprints=blueprints)

        app.register_blueprint.assert_has_calls([
            mock.call('foo', 'arg1', 'arg2')
        ])

    def test_can_handle_simple_strings_inside_iterables_as_well(self):
        app = self.generate_app()
        foo = stub_blueprint('foo')
        with mock.patch.object(helpers, 'import_string') as import_string:
            import_string.side_effect = [foo, ]
            blueprints = [
                ['foo', ],
            ]
            helpers.setup_blueprints(app, blueprints=blueprints)

        app.register_blueprint.assert_has_calls([mock.call('foo')])
