from .serializers import DetailSerializer
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


class Schema:
    def __init__(
        self,
        method=None,
        methods=None,
        response_200=None,
        response_201=None,
        response_400=DetailSerializer,
        response_401=DetailSerializer,
        response_403=DetailSerializer,
        response_404=DetailSerializer,
        response_500=None,
        query_serializer=None,
        request_body=None,
    ):
        self.method = method
        self.methods = methods
        self.response_200 = response_200
        self.response_201 = response_201
        self.response_400 = response_400
        self.response_401 = response_401
        self.response_403 = response_403
        self.response_404 = response_404
        self.response_500 = response_500

        if response_500:
            self.response_500 = response_500  # pragma: no cover
        elif 500 in settings.HELPERS.get("ERROR_CODES_TO_CATCH", []):
            self.response_500 = DetailSerializer
        else:
            self.response_500 = None  # pragma: no cover

        self.query_serializer = query_serializer
        self.request_body = request_body

    def get_responses(self):
        responses = {
            200: self.response_200,
            201: self.response_201,
            400: self.response_400,
            401: self.response_401,
            403: self.response_403,
            404: self.response_404,
            500: self.response_500,
        }
        for code in settings.HELPERS.get("ERROR_CODES_TO_CATCH", []):
            responses[code] = DetailSerializer
        return responses

    def to_swagger_auto_schema_dict(self):
        return {
            "method": self.method,
            "methods": self.methods,
            "responses": self.get_responses(),
            "query_serializer": self.query_serializer,
            "request_body": self.request_body,
        }

    def __call__(self, func):
        return swagger_auto_schema(**self.to_swagger_auto_schema_dict())(func)


healthcheck_schema = Schema(methods=["GET"], response_200=DetailSerializer)
