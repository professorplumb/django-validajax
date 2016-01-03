from __future__ import unicode_literals

import json

from django.forms import ValidationError
from django.http import HttpResponse
from django.views.generic import View

from . import form_registry
from .registration import KeyNotFound


class FieldValidationView(View):
    def make_response(self, dct, status=200):
        return HttpResponse(json.dumps(dct), content_type='application/json', status=status)

    def make_failure_response(self, message):
        return self.make_response({'success': False, 'message': message})

    def make_error_response(self, message, status=500):
        return self.make_response({'success': False, 'message': message}, status=status)

    def get(self, *args, **kwargs):
        form_key = self.kwargs['form_key']
        field_name = self.kwargs['field_name']
        try:
            form_class = form_registry.get_form_class_from_namespace(form_key)
            form_obj = form_class({field_name: self.request.GET.get('val')})
            cleaned_value = getattr(form_obj, 'clean_{}'.format(field_name))()
            response_message = form_registry.get_response_message(form_obj, field_name, cleaned_value)
        except KeyNotFound as e:
            return self.make_error_response(e.message)
        except ValidationError as e:
            return self.make_failure_response(e.message)

        resp = {'success': True}
        if response_message is not None:
            resp['message'] = response_message
        return self.make_response(resp)
