import mock
import json

from unittest import TestCase

from django.forms import ValidationError

from .. import form_registry
from ..views import FieldValidationView


class FieldValidationViewTests(TestCase):
    class MockForm(object):
        def __init__(self, *args, **kwargs):
            pass

        def clean_name(self):
            return None

        def clean_wrong_name(self):
            raise ValidationError("Wrong name!")

    def setUp(self):
        super(FieldValidationViewTests, self).setUp()

        self.view = FieldValidationView()
        self.form_class = self.MockForm
        form_registry.register(self.form_class, namespace='mock-form')

    def test_returns_success_response_if_successful(self):
        self.view.kwargs = dict(form_key='mock-form', field_name='name')
        self.view.request = mock.Mock(GET=dict(val='value'))
        response = self.view.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'success': True})

    def test_adds_success_message_if_provided(self):
        self.view.kwargs = dict(form_key='mock-form', field_name='name')
        self.view.request = mock.Mock(GET=dict(val='value'))
        with mock.patch.object(form_registry, 'get_response_message', return_value="Name!"):
            response = self.view.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                json.loads(response.content),
                {'success': True, 'message': "Name!"})

    def test_returns_failure_response_if_validation_fails(self):
        self.view.kwargs = dict(form_key='mock-form', field_name='wrong_name')
        self.view.request = mock.Mock(GET=dict(val='value'))
        response = self.view.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'success': False, 'message': "Wrong name!"})

    def test_returns_error_response_if_field_not_present_on_form(self):
        self.view.kwargs = dict(form_key='mock-form', field_name='wrong_field')
        self.view.request = mock.Mock(GET=dict(val='value'))
        response = self.view.get()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            json.loads(response.content),
            {
                'success': False,
                'message': ("'{}' object has no attribute 'clean_wrong_field'".format(self.form_class.__name__)),
            })

    def test_returns_error_response_if_form_not_registered(self):
        self.view.kwargs = dict(form_key='wrong-form', field_name='unimportant')
        self.view.request = mock.Mock(GET=dict(val='value'))
        response = self.view.get()
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            json.loads(response.content),
            {
                'success': False,
                'message': ("'wrong-form' not found in Django-ValidAJAX namespace registry."
                            " Have you registered your form?"),
            })
