import inspect

from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.forms import BaseForm

from . import form_registry


class DjangoValidAJAXAppConfig(AppConfig):
    name = 'django_validajax'
    verbose_name = 'Django-ValidAJAX'

    @staticmethod
    def _is_form_class(obj):
        return inspect.isclass(obj) and issubclass(obj, BaseForm)

    def ready(self):
        should_autoregister = getattr(settings, 'VALIDAJAX_CONFIG', {}).get('AUTOREGISTER', False)
        if not should_autoregister:
            return

        for app_name in settings.INSTALLED_APPS:
            if app_name.startswith('django.'):
                continue

            try:
                forms_module = import_module('{}.forms'.format(app_name))
                for _, form_class in inspect.getmembers(forms_module, self._is_form_class):
                    form_registry.register(form_class, autoregistered=True)
            except ImportError:
                pass
