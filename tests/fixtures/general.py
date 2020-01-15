from functools import wraps

import pytest
from rest_framework.test import RequestsClient


def _decorate_app_methods(
    app, methods_to_decorate=("get", "post", "put", "patch", "delete", "head")
):
    def decorate_method(method):
        @wraps(method)
        def wrapper(address, *args, **kwargs):
            return method(f"http://testserver{address}", *args, **kwargs)

        return wrapper

    for method_name in methods_to_decorate:
        method = getattr(app, method_name)
        method = decorate_method(method)
        setattr(app, method_name, method)
    return app


@pytest.fixture
def drf_client():
    """
    This is fixture is client which allows you to test REST api provided by application
    using requests like interface.
    For example you can use this fixture as follows:
        ```
        response = app.get('/my_cool_url/').json()
        assert response.get('details') == 'Some value'
        ```
    """
    client = RequestsClient()
    client = _decorate_app_methods(client)
    return client
