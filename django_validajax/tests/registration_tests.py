import mock

from unittest import TestCase

from ..registration import FormRegistry, FormNotFound, KeyNotFound


class FormRegistryTests(TestCase):
    def setUp(self):
        super(FormRegistryTests, self).setUp()

        self.registry = FormRegistry()
        self.form = mock.Mock()

    def test_registers_form_class_to_namespace(self):
        self.registry.register(self.form.__class__, namespace='ns')
        self.assertEqual(self.registry.get_namespace_from_form(self.form.__class__), 'ns')

    def test_registers_form_to_namespace_via_class(self):
        self.registry.register(self.form, namespace='ns')
        self.assertEqual(self.registry.get_namespace_from_form(self.form.__class__), 'ns')

    def test_returns_namespace_via_form_object_as_well(self):
        self.registry.register(self.form, namespace='ns')
        self.assertEqual(self.registry.get_namespace_from_form(self.form), 'ns')

    def test_raises_formnotfound_if_wrong_form_class(self):
        self.registry.register(self.form)
        with self.assertRaises(FormNotFound):
            self.registry.get_namespace_from_form(mock.Mock())

    def test_returns_form_class_via_namespace(self):
        self.registry.register(self.form, namespace='ns')
        self.assertEqual(self.registry.get_form_class_from_namespace('ns'), self.form.__class__)

    def test_raises_keynotfound_if_wrong_namespace(self):
        self.registry.register(self.form, namespace='ns')
        with self.assertRaises(KeyNotFound):
            self.registry.get_form_class_from_namespace('not-a-namespace')

    def test_defaults_namespace_to_attribute_on_form_class(self):
        self.form.__class__.validajax_namespace = 'validajax-namespace'
        self.registry.register(self.form)
        self.assertEqual(self.registry.get_namespace_from_form(self.form.__class__), 'validajax-namespace')

    def test_assigns_random_string_otherwise(self):
        with mock.patch.object(self.registry, '_determine_namespace_from_form_class', return_value='as3c8iduf'):
            self.registry.register(self.form)
            self.assertEqual(self.registry.get_namespace_from_form(self.form.__class__), 'as3c8iduf')

    def test_registers_response_callback(self):
        self.registry.register(self.form, success_message=lambda *_: "Success!")
        self.assertEqual(
            self.registry.get_response_message(self.form, mock.Mock(), mock.Mock()),
            "Success!")

    def test_response_callback_returns_none_if_registered_as_none(self):
        self.registry.register(self.form, success_message=None)
        self.assertIsNone(self.registry.get_response_message(self.form, mock.Mock(), mock.Mock()))

    def test_response_callback_returns_cleaned_value_if_registered_as_true(self):
        self.registry.register(self.form, success_message=True)
        self.assertEqual(
            self.registry.get_response_message(self.form, mock.Mock(), "cleaned value"),
            "cleaned value")

    def test_response_callback_returns_called_value_if_registered_as_callable(self):
        self.registry.register(self.form, success_message=lambda f, fn, val: "{}.{}: {}".format(str(f), fn, val))
        self.assertEqual(
            self.registry.get_response_message(self.form, 'fieldname', 'cleaned value'),
            "{}.fieldname: cleaned value".format(str(self.form)))

    def test_response_callback_returns_registered_value_if_registered_as_anything_else(self):
        self.registry.register(self.form, success_message=mock.sentinel)
        self.assertEqual(
            self.registry.get_response_message(self.form, mock.Mock(), mock.Mock()),
            mock.sentinel)

    def test_response_callback_defaults_to_attribute_on_form_class_if_none(self):
        self.form.__class__.validajax_success_callback = mock.sentinel
        self.registry.register(self.form, success_message=None)
        self.assertEqual(
            self.registry.get_response_message(self.form, mock.Mock(), mock.Mock()),
            mock.sentinel)

    @mock.patch('django_validajax.registration.logger.info')
    def test_logs_registration(self, info_mock):
        self.registry.register(self.form, namespace='my-namespace')
        info_mock.assert_called_once_with(
            "Registering %s as namespace %s",
            self.form.__class__,
            'my-namespace')