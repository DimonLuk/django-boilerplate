from django.conf import settings
from rest_framework import serializers


class MetaInfoInnerSerializerMixin(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            "helpers.middleware.ResponseMetaInformationInJsonMiddleware"
            in settings.MIDDLEWARE
        ):
            if "version" in settings.HELPERS.get("META_INFO", []):
                self.fields["application_version"] = serializers.CharField(
                    read_only=True
                )

            if "timestamp" in settings.HELPERS.get("META_INFO", []):
                self.fields["timestamp"] = serializers.CharField(
                    read_only=True
                )

            if "hash" in settings.HELPERS.get("META_INFO", []):
                self.fields["response_hash"] = serializers.CharField(
                    read_only=True
                )


class MetaInfoSerializerMixin(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            "helpers.middleware.ResponseMetaInformationInJsonMiddleware"
            in settings.MIDDLEWARE
        ):
            self.fields["_meta_info"] = MetaInfoInnerSerializerMixin(
                read_only=True
            )


class DetailSerializer(MetaInfoSerializerMixin, serializers.Serializer):
    detail = serializers.CharField(read_only=True)
