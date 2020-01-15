from django.db import connections
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from .schemas import healthcheck_schema


@healthcheck_schema
@api_view(("GET",))
@authentication_classes(())
@permission_classes(())
def healthcheck(request):
    connection = connections["default"]
    connection.cursor()
    return Response({"detail": "Everything works"}, status=status.HTTP_200_OK)
