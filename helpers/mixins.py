from django.conf import settings


class IsIncludeMetaInfoMixin:
    @property
    def _is_include_meta_info(self):
        return (
            "helpers.middleware.ResponseMetaInformationInJsonMiddleware"
            in settings.MIDDLEWARE
        )
