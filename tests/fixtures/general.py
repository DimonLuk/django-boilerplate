from functools import wraps

import pytest
from rest_framework.test import RequestsClient


@pytest.fixture
def app(django_app_factory):
    client = django_app_factory(csrf_checks=False, extra_environ={})
    return client
