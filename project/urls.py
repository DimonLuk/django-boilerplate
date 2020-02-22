"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from allauth.account.views import ConfirmEmailView
from rest_framework_jwt.views import refresh_jwt_token


api_info = openapi.Info(
    title="Project name",
    default_version=f"v{settings.HELPERS['APPLICATION_VERSION']}",
    description="Project swagger",
    contact=openapi.Contact(email="dimonluk2.0@gmail.com"),
)

schema_view = get_schema_view(
    public=True, url=settings.HELPERS["PROJECT_URL"],
)


if settings.HELPERS["SWAGGER_SCHEMA_NO_AUTH"]:
    schema_view.authentication_classes = ()
    schema_view.permission_classes = ()


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("helpers/", include("helpers.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("grappelli/", include("grappelli.urls")),
    path("accounts/", include("allauth.urls")),
    re_path(
        r"^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("rest-auth/refresh-token", refresh_jwt_token),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
]
