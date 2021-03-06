# Django-ValidAJAX

Set up validation endpoints for (ValidAJAX)[https://github.com/professorplumb/ValidAJAX] in your Django project.

## Installation

1. Add `django_validajax` to `settings.INSTALLED_APPS`
1. Use `settings.VALIDAJAX_CONFIG` to customize your installation (see [Settings](#django-settings) below)
1. Include `django_validajax.urls` in your main `urls.py`.  You can use any prefix you like in `include()`, but
   you need to give it the `namespace='django-validajax'` kwarg.  E.g. 
   `(r'^this/prefix/doesnt/matter/, include('django_validajax.urls', namespace='django-validajax'))`
1. Register each form class you want to validate.  Either set `settings.VALIDAJAX_CONFIG['AUTOREGISTER']` to `True`, or
   call `form_registry.register(MyFormClass)` for each individual form class.  See
   [Form Registration](#form-registration) below for options.)
1. On each template where you need to validate one or more forms:
   1. `{% load django_validajax %}` at the top of your template.
   1. Include the `{% initialize_validajax %}` template tag before the closing `body` tag, which will call `ValidAJAX.init()`
      with options generated from your settings.
   1. For each form you want to validate, include `validate="true"` in the `form` tag (or something else which will
      match [`settings.VALIDAJAX_CONFIG['FORM_SELECTOR']`](#form_selector)), and also
      `data-validajax-namespace={% validation_url_for form %}` (the `form` context variable should contain either
      your form or its class.)

## Form Registration

### `form_registry.register`

```python
from django_validajax import form_registry

class MyForm(ModelForm):
    ...
    
def success_message_func(form, field_name, value):
    if field_name == 'name':
        return value
    elif field_name == 'nemesis_name':
        return value[::-1]
    
registry.register(MyForm, namespace='myform_namespace', success_message=success_message_func)
```

`registry.register` will register (surprise!) your form class with Django-ValidAJAX so it can be looked up by its
namespace.  It takes one argument and two optional kwargs:

1. `form_class` (required).  The class (or an instance) of the form you want to register.
1. `namespace` (optional).  A string, valid in a URL, which will map to this form in the validation URL pattern.
   Defaults to a 10-character random string.
1. `success_message` (optional).  `None`, a boolean, or a function.  Determines whether a message will be returned on
   success for this form (a message is always returned on failure.)
   1. `None` or `False`: no success message is returned for any field.
   1. `True`: the field's value will be returned on success.
   1. `func(form, field_name, cleaned_value)`: set up this function to return anything you'd like.  Arguments are the
      form instance, field name under validation, and the value returned by `clean_{fieldname}`.  The example above
      returns the value unaltered for the `name` field, and the value reversed for the `nemesis_name` field.

You can also choose to set `namespace` and `success_message` on the form class itself via the `validajax_namespace` and
`validajax_success_message` attributes:

```python

class MyForm(ModelForm):
    validajax_namespace = 'myform_namespace'
    validajax_success_callback = success_message_func
```

### Autoregistration

If you wish, you can have Django-ValidAJAX look up and register your forms for you.  It's not all that smart: it just
looks in all of your non-DJANGO `INSTALLED_APPS` for a `forms` module and registers everything that looks like a form
from there.  You will also have to use attributes on the form class if you want a custom namespace or success callback;
see above for details.

If a form is already autoregistered and you call `registry.register` explicitly, your explicit values will take
precedence.

To enable autoregistration, set `settings.VALIDAJAX_CONFIG['AUTOREGISTER']` to a truthy value.  **Autoregistration is
only available in Django 1.7 and above.**

## Customization

### Django settings

To override Django-ValidAJAX's defaults, add a dictionary to your `settings.py` named `VALIDAJAX_CONFIG` with one or
more of the following keys:

#### `AUTOREGISTER`

Turns [autoregistration](#autoregistration) on if set to anything evaluating to a truthy value.  Defaults to off.

#### `FORM_SELECTOR`

A CSS-style selector which determines which forms on a page will be validated.  Maps to and overrides ValidAJAX's 
[formSelector](https://github.com/professorplumb/ValidAJAX#formselector) option.

#### `INPUT_SELECTOR`

A CSS-style selector which determines which inputs within a form will be validated.  Maps to and overrides ValidAJAX's
[inputSelector](https://github.com/professorplumb/ValidAJAX#inputselector) option.

