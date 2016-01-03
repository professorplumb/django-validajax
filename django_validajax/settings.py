import sys

from django.conf import settings

_defaults = [
    ('FORM_SELECTOR', None, 'formSelector'),
    ('INPUT_SELECTOR', None, 'inputSelector'),
]

JS_KEY_MAP = {}

_override_settings = getattr(settings, 'VALIDAJAX_CONFIG', {})
for setting_name, default_value, js_key in _defaults:
    # set a local setting for use by Django-ValidAJAX
    setattr(
        sys.modules[__name__],
        setting_name,
        _override_settings.get(setting_name, default_value))

    # save mapping from setting name to config attribute name for ValidAJAX.init() in Javascript
    if js_key:
        JS_KEY_MAP[setting_name] = js_key
