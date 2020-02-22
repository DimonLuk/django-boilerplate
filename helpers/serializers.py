from django.conf import settings
from rest_framework import serializers

from .mixins import IsIncludeMetaInfoMixin


class MetaInfoInnerSerializerMixin(
    IsIncludeMetaInfoMixin, serializers.Serializer
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._include_verion_if_required()
        self._include_timestamp_if_required()
        self._include_hash_if_required()

    def _include_verion_if_required(self):
        if self._is_include_meta_info and self._is_include_version:
            self.fields["application_version"] = serializers.CharField(
                read_only=True
            )

    def _include_timestamp_if_required(self):
        if self._is_include_meta_info and self._is_include_timestamp:
            self.fields["timestamp"] = serializers.DateTimeField(
                read_only=True
            )

    def _include_hash_if_required(self):
        if self._is_include_meta_info and self._is_include_hash:
            self.fields["hash"] = serializers.CharField(read_only=True)

    @property
    def _is_include_version(self):
        return "version" in self._meta_info

    @property
    def _is_include_timestamp(self):
        return "timestamp" in self._meta_info

    @property
    def _is_include_hash(self):
        return "hash" in self._meta_info

    @property
    def _meta_info(self):
        return settings.HELPERS.get("META_INFO", [])


class MetaInfoSerializerMixin(IsIncludeMetaInfoMixin, serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._include_inner_meta_info_if_required()

    def _include_inner_meta_info_if_required(self):
        if self._is_include_meta_info:
            self.fields["_meta_info"] = MetaInfoInnerSerializerMixin(
                read_only=True
            )


class DetailSerializer(MetaInfoSerializerMixin, serializers.Serializer):
    detail = serializers.CharField(read_only=True)
