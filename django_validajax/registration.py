from __future__ import unicode_literals

import inspect
import logging
import string
import random

logger = logging.getLogger('django-validajax')


class KeyNotFound(Exception):
    pass


class FormNotFound(Exception):
    pass


class FormRegistry(object):
    """
    Keeps a record of all forms registered.
    """
    def __init__(self):
        self._class_registry = {}
        self._key_registry = {}
        self._response_registry = {}

    def register(self, form, namespace=None, success_message=None, autoregistered=False):
        form_class = form if inspect.isclass(form) else form.__class__

        # short-circuit multiple registration unless the previous one was automatic,
        # to allow manual registrations to override autoregistration
        if form_class in self._class_registry and self._class_registry[form_class][1] is not True:
            return

        if namespace is None:
            namespace = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))
        logger.info("Registering %s as namespace %s", form_class, namespace)
        self._key_registry[namespace] = form_class
        self._class_registry[form_class] = (namespace, autoregistered)
        self._response_registry[form_class] = success_message

    def get_form_class_from_namespace(self, namespace):
        try:
            return self._key_registry[namespace]
        except KeyError:
            raise KeyNotFound(
                "'{}' not found in Django-ValidAJAX namespace registry."
                " Have you registered your form?".format(namespace))

    def get_namespace_from_form(self, form):
        form_class = form if inspect.isclass(form) else form.__class__
        try:
            return self._class_registry[form_class][0]
        except KeyError:
            raise FormNotFound(
                "'{}' not found in Django-ValidAJAX registry."
                " Have you registered your form?".format(form))

    def get_response_message(self, form, field_name, cleaned_value):
        form_class = form if inspect.isclass(form) else form.__class__
        response_obj = self._response_registry.get(form_class)
        if not response_obj:
            return None
        elif response_obj is True:
            return cleaned_value
        elif callable(response_obj):
            return response_obj(form, field_name, cleaned_value)

        return response_obj
