from __future__ import unicode_literals

import json

from django import template
from django.conf import settings as django_settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .. import form_registry, settings as validajax_settings

register = template.Library()


@register.simple_tag
def validation_namespace_for(form):
    return form_registry.get_namespace_from_form(form)


@register.simple_tag
def initialize_validajax():
    dummy_validation_url = reverse('validajax:validate-single-formfield', args=['foo', 'bar'])
    options = dict(
        debugOptions=django_settings.DEBUG,
        validationURLPrefix='/'.join(dummy_validation_url.split('/')[:-2]),
    )

    # we don't send these to ValidAJAX unless the user has overriden them
    for overridable_setting_name, js_key in validajax_settings.JS_KEY_MAP.iteritems():
        setting_value = getattr(validajax_settings, overridable_setting_name, None)
        if setting_value:
            options[js_key] = setting_value

    return mark_safe("""<script type="text/javascript">
        ValidAJAX.init(JSON.parse('{}'));
    </script>""".format(json.dumps(options)))
