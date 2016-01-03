from django.conf.urls import patterns, url

from .views import FieldValidationView

urlpatterns = patterns(
    '',
    url(
        r'^(?P<form_key>[\w\d\._-]+)/(?P<field_name>[\w\d_-]+)/?$',
        FieldValidationView.as_view(),
        name='validate-single-formfield')
)
