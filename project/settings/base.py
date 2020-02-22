import os


# HELPERS SETTINGS
HELPERS = {
    "SELF_STATIC_SERVE": True,
    "PROJECT_URL": "http://localhost:8000",
    "SWAGGER_SCHEMA_NO_AUTH": True,
    "INCLUDE_META_INFO": True,
    "META_INFO": ["version", "hash", "timestamp"],
    "APPLICATION_VERSION": "0.0.1",
    "ERROR_CODES_TO_CATCH": [500],
    "SUPERUSER_EMAILS": [],
    "SUPERUSER_USERNAMES": ["admin"],
    "ENABLE_DEBUG_TOOLBAR": True,
}
MODE = os.environ.get("MODE")


# DEFAULT DJANGO SETTINGS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
SECRET_KEY = "override"
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "corsheaders",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "rest_auth.registration",
    "drf_yasg",
    "helpers",
    "debug_toolbar",
]
SITE_ID = 1
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "helpers.middleware.ResponseMetaInformationInHeadersMiddleware",
    "helpers.middleware.ResponseMetaInformationInJsonMiddleware",
    "helpers.middleware.ErrorFormatterMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
ROOT_URLCONF = "project.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "project.wsgi.application"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # NOQA
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = "/helpers/static/"


# DRF SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ]
}


# DJANGO CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = True


# DJANGO REST AUTH SETTINGS
REST_USE_JWT = True
JWT_AUTH = {"JWT_AUTH_HEADER_PREFIX": "Bearer", "JWT_ALLOW_REFRESH": True}
OLD_PASSWORD_FIELD_ENABLED = True


# DJANGO ALLAUTH SETTINGS
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"


# DRF YASG SETTINGS
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "DEFAULT_INFO": "project.urls.api_info",
}


# DEBUG TOOLBAR SETTINGS
class IsToolbarVisibleChecker:
    def __call__(self, request):
        user = self._get_user(request)
        result = self._not_ajax(request)
        result &= self._env_variable_set_to_true
        result &= self._check_user_satisfies_conditions(result, user)
        return result

    def _get_user(self, request):
        return getattr(request, "user", None)

    def _not_ajax(self, request):
        return not request.is_ajax()

    @property
    def _env_variable_set_to_true(self):
        return HELPERS.get("ENABLE_DEBUG_TOOLBAR", False)

    def _check_user_satisfies_conditions(self, result, user):
        if result and user:
            username = getattr(user, "username", None)
            email = getattr(user, "email", None)
            return self._is_superuser(username, email)
        else:
            return False

    def _is_superuser(self, username, email):
        return username in HELPERS.get(
            "SUPERUSER_USERNAMES", []
        ) or email in HELPERS.get("SUPERUSER_EMAILS", [])


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": IsToolbarVisibleChecker(),
}


# GRAPELLI SETTINGS
GRAPPELLI_ADMIN_TITLE = "Project title"
