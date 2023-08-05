import inspect
import os
from json import loads as json_loads

from django import template
from django.template import defaultfilters

register = template.Library()

DEBUG_DJANGO_BONUS = os.getenv("DJANGO_BONUS_DEBUG") in [True, "True", "true", "TRUE"]

NAMES_OF_DEFAULT_FILTERS = dir(defaultfilters)
if DEBUG_DJANGO_BONUS:
    print("NAMES_OF_DEFAULT_FILTERS:", NAMES_OF_DEFAULT_FILTERS)


def register_string_method(string_method):
    try:
        if DEBUG_DJANGO_BONUS:
            print("[django-bonus] registering " + string_method)
        register.filter(
            string_method,
            lambda value, arg="[]": getattr(value, string_method)(*json_loads(arg)),
        )
        # if DEBUG_DJANGO_BONUS:
        # print(f"[django-bonus] {string_method} filter is", register.filters[string_method])

        # if string_method not in register.filters:
        # print("[django-bonus] failed to register " + string_method)

    except Exception as e:
        print("[django-bonus] exception while registering " + string_method, e)


for string_method in dir(""):
    if not string_method.startswith("_"):
        if string_method not in NAMES_OF_DEFAULT_FILTERS:
            register_string_method(string_method)
