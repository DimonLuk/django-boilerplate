from django.conf import settings
from django.urls import path, re_path, include

from .views import healthcheck
import debug_toolbar

urlpatterns = [
    path("healthcheck/", healthcheck, name="healthcheck"),
]

if settings.MODE in ("dev", "qa", "prod") and settings.HELPERS.get(
    "SELF_STATIC_SERVE", False
):
    from django.views.static import serve

    urlpatterns.append(
        re_path(
            "^static/(?P<path>.*)$",
            serve,
            {"document_root": settings.STATIC_ROOT},
        )
    )


if settings.HELPERS.get("ENABLE_DEBUG_TOOLBAR", False):
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)),)
