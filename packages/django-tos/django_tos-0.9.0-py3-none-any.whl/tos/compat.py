import django
from django.conf import settings
from django.utils import deprecation


def patterns(mod, *urls):
    if mod != '' or django.VERSION < (1, 9):
        from django.conf.urls import patterns
        return patterns(mod, *urls)
    else:
        return list(urls)


def get_fk_user_model():
    if django.VERSION >= (1, 5):
        return settings.AUTH_USER_MODEL
    from django.contrib.auth.models import User
    return User


def get_runtime_user_model():
    if django.VERSION >= (1, 5):
        from django.contrib.auth import get_user_model
        return get_user_model()
    from django.contrib.auth.models import User
    return User


def get_request_site():
    if django.VERSION >= (1, 9):
        from django.contrib.sites.requests import RequestSite
    else:
        from django.contrib.sites.models import RequestSite
    return RequestSite


def get_library():
    if django.VERSION >= (1, 9):
        from django.template.library import Library
    else:
        from django.template.base import Library
    return Library


def get_cache(cache_name):
    if django.VERSION >= (1, 7):
        from django.core.cache import caches
        return caches[cache_name]
    else:
        from django.core.cache import get_cache
        return get_cache(cache_name)


def get_middleware_mixin():
    if django.VERSION >= (1, 10, 0):
        return deprecation.MiddlewareMixin
    else:
        return object


def get_middleware_settings_key():
    if django.VERSION >= (1, 10, 0):
        return 'MIDDLEWARE'
    else:
        return 'MIDDLEWARE_CLASSES'


if django.VERSION < (1, 5):
    from django.templatetags.future import url
else:
    from django.template.defaulttags import url

if django.VERSION >= (1, 10, 0):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse
