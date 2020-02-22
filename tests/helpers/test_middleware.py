import pytest
from django.http import JsonResponse
from helpers.middleware import (
    ErrorFormatterMiddleware,
    ResponseMetaInformationInJsonMiddleware,
    ResponseMetaInformationInHeadersMiddleware,
)
import json
from freezegun import freeze_time


@pytest.fixture
def get_error_response():
    def _inner(request):
        return JsonResponse({"error": "Some error"}, status=500)

    return _inner


@pytest.fixture
def get_success_response():
    def _inner(request):
        return JsonResponse({"detail": "Everything works"}, status=200)

    return _inner


def test_error_formatter_middleware(get_error_response, settings):
    settings.HELPERS["ERROR_CODES_TO_CATCH"] = [500]
    settings.DEBUG = False
    middleware = ErrorFormatterMiddleware(get_error_response)
    response = middleware(None)
    assert response.status_code == 500
    assert json.loads(response.content) == {"detail": "Internal server error"}


def test_error_formatter_middleware_success_response(
    get_success_response, settings
):
    settings.HELPERS["ERROR_CODES_TO_CATCH"] = [500]
    settings.DEBUG = False
    middleware = ErrorFormatterMiddleware(get_success_response)
    response = middleware(None)
    assert response.status_code == 200
    assert json.loads(response.content) == {"detail": "Everything works"}


@freeze_time("2020-01-01")
def test_response_meta_info_in_json(get_success_response, settings, snapshot):
    settings.HELPERS.update(
        {
            "INCLUDE_META_INFO": True,
            "META_INFO": ["version", "hash", "timestamp"],
        }
    )
    middleware = ResponseMetaInformationInJsonMiddleware(get_success_response)
    response = middleware(None)
    assert response.status_code == 200
    snapshot.assert_match(json.loads(response.content), "Meta info in json")


@freeze_time("2020-01-01")
def test_response_meta_info_in_headers(
    get_success_response, settings, snapshot
):
    settings.HELPERS.update(
        {
            "INCLUDE_META_INFO": True,
            "META_INFO": ["version", "hash", "timestamp"],
        }
    )
    settings.DEBUG = False
    middleware = ResponseMetaInformationInHeadersMiddleware(
        get_success_response
    )
    response = middleware(None)
    assert response.status_code == 200
    snapshot.assert_match(json.loads(response.content), "Response")
    snapshot.assert_match(response._headers, "Meta info with headers")


@pytest.mark.parametrize(
    "middleware_class",
    [
        ResponseMetaInformationInHeadersMiddleware,
        ResponseMetaInformationInJsonMiddleware,
    ],
)
@freeze_time("2020-01-01")
def test_not_response_meta_info(
    get_success_response, settings, snapshot, middleware_class
):
    settings.HELPERS.update({"INCLUDE_META_INFO": False})
    settings.DEBUG = False
    middleware = middleware_class(get_success_response)
    response = middleware(None)
    assert response.status_code == 200
    snapshot.assert_match(json.loads(response.content), "Response")
    snapshot.assert_match(response._headers, "Meta info with headers")
