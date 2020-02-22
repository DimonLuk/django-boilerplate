import datetime
import hashlib
import json
from django.http import JsonResponse

from django.conf import settings


class ErrorFormatterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if self._is_response_to_catch(response):
            response = JsonResponse(
                {"detail": "Internal server error"},
                status=response.status_code,
            )
        return response

    def _is_response_to_catch(self, response):
        return (
            response.status_code
            in settings.HELPERS.get("ERROR_CODES_TO_CATCH", [])
            and not settings.DEBUG
        )


class _BaseResponseMetaInformationMiddleware:
    version_field = None
    timestamp_field = None
    hash_field = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self._modify_response(response)
        return response

    def _modify_response(self, response):
        self._include_version(response)
        self._include_timestamp(response)
        self._include_hash(response)

    def _include_version(self, response):
        if self._is_include_meta_info and self._is_include_version:
            response[self.version_field] = self._get_appicaltion_version()

    def _include_timestamp(self, response):
        if self._is_include_meta_info and self._is_include_timestamp:
            response[self.timestamp_field] = self._get_timestamp()

    def _include_hash(self, response):
        if self._is_include_meta_info and self._is_include_hash:
            response[self.hash_field] = self._get_hash(response)

    @property
    def _is_include_meta_info(self):
        return settings.HELPERS.get("INCLUDE_META_INFO", False)

    @property
    def _is_include_version(self):
        return "version" in settings.HELPERS.get("META_INFO", [])

    @property
    def _is_include_timestamp(self):
        return "timestamp" in settings.HELPERS.get("META_INFO", [])

    @property
    def _is_include_hash(self):
        return "hash" in settings.HELPERS.get("META_INFO", [])

    def _get_appicaltion_version(self):
        return settings.HELPERS["APPLICATION_VERSION"]

    def _get_timestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _get_hash(self, response):
        response_hash = self._get_timestamp() + str(response)
        return hashlib.md5(response_hash.encode()).hexdigest()


class ResponseMetaInformationInHeadersMiddleware(
    _BaseResponseMetaInformationMiddleware
):
    version_field = "H-Application-Version"
    timestamp_field = "H-Timestamp"
    hash_field = "H-Response-Hash"


class ResponseMetaInformationInJsonMiddleware(
    _BaseResponseMetaInformationMiddleware
):
    version_field = "application_version"
    timestamp_field = "timestamp"
    hash_field = "hash"

    def _modify_response(self, response):
        json_data = self._get_json_data(response)

        if json_data and self._is_include_meta_info:
            meta_info = {}

            self._include_version(meta_info)
            self._include_timestamp(meta_info)
            self._include_hash(meta_info)

            json_data["_meta_info"] = meta_info
            response.content = json.dumps(json_data).encode()

    def _get_json_data(self, response):
        try:
            return self._extract_json_data_from_response(response)
        except Exception:  # pragma: no cover
            return None  # pragma: no cover

    def _extract_json_data_from_response(self, response):
        raw_content = response.content
        json_data = json.loads(raw_content)
        return json_data
