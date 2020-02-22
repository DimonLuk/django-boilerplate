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
        if (
            response.status_code
            in settings.HELPERS.get("ERROR_CODES_TO_CATCH", [])
            and not settings.DEBUG
        ):
            response = JsonResponse(
                {"detail": "Internal server error"},
                status=response.status_code,
            )
        return response


class ResponseMetaInformationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.HELPERS.get("INCLUDE_META_INFO", None):
            timestamp = datetime.datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )

            if settings.HELPERS.get("META_INFO_IN_HEADERS", None):

                if "version" in settings.HELPERS.get("META_INFO", []):
                    response["H-Application-Version"] = settings.HELPERS[
                        "APPLICATION_VERSION"
                    ]

                if "timestamp" in settings.HELPERS.get("META_INFO", []):
                    response["H-Timestamp"] = timestamp

                if "hash" in settings.HELPERS.get("META_INFO", []):
                    response_hash = timestamp + str(response)
                    response_hash = hashlib.md5(
                        response_hash.encode()
                    ).hexdigest()
                    response["H-Response-Hash"] = response_hash

            elif settings.HELPERS.get("META_INFO_IN_JSON_RESPONSE", None):

                meta_info = {}

                try:
                    raw_content = response.content
                    json_data = json.loads(raw_content)
                except Exception:  # pragma: no cover
                    return response  # pragma: no cover

                if "version" in settings.HELPERS.get("META_INFO", []):
                    meta_info["application_version"] = settings.HELPERS[
                        "APPLICATION_VERSION"
                    ]

                if "timestamp" in settings.HELPERS.get("META_INFO", []):
                    meta_info["timestamp"] = timestamp

                if "hash" in settings.HELPERS.get("META_INFO", []):
                    response_hash = timestamp + json.dumps(json_data)
                    response_hash = hashlib.md5(
                        response_hash.encode()
                    ).hexdigest()
                    meta_info["response_hash"] = hashlib.md5(
                        response_hash.encode()
                    ).hexdigest()
                json_data["_meta_info"] = meta_info
                response.content = json.dumps(json_data).encode()

        return response
