from pathlib import Path

import environ

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, "forlocaltest"),
    CORS_ALLOWED_ORIGIN_REGEXES=(list, None),
    CSRF_TRUSTED_ORIGINS=(list, None),
)

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGIN_REGEXES = env(
    "CORS_ALLOWED_ORIGIN_REGEXES",
)

if env("CSRF_TRUSTED_ORIGINS"):
    CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    # Daisy UI Admin
    "django_daisy",
    "django.contrib.humanize",
    # Original Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # API
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # Core Configurations
    "core.api",
    "core.swagger",
    "image_uploader_widget",
    # Feature Apps
    "features.authentication",
    "features.user",
    "features.stores",
]

AUTH_USER_MODEL = "user.User"
AUTHENTICATION_BACKENDS = ["features.authentication.backends.ModelBackend"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env("DB_HOST"),
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PORT": env("DB_PORT"),
        "PASSWORD": env("DB_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"


STATIC_ROOT = Path.joinpath(BASE_DIR, "static")
MEDIA_ROOT = Path.joinpath(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Cifra Marketplace API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "TAGS": [
        {
            "name": "auth",
            "description": "Reúne endpoints para lidar com autenticação por JWT.",
        },
        {
            "name": "users",
            "description": "Reúne endpoints para lidar com os usuários da plataforma.",
        },
    ],
}

DAISY_SETTINGS = {
    "SITE_TITLE": "Cifra Marketplace Admin",  # The title of the site
    "SITE_HEADER": "Administração",  # Header text displayed in the admin panel
    # 'INDEX_TITLE': 'Hi, welcome to your dashboard',  # The title for the index page of dashboard
    # 'SITE_LOGO': '/static/admin/cifra-logo.png',  # Path to the logo image displayed in the sidebar
    "EXTRA_STYLES": [],  # List of extra stylesheets to be loaded in base.html (optional)
    "EXTRA_SCRIPTS": [],  # List of extra script URLs to be loaded in base.html (optional)
    "LOAD_FULL_STYLES": False,  # If True, loads full DaisyUI components in the admin (useful if you have custom template overrides)
    "SHOW_CHANGELIST_FILTER": False,  # If True, the filter sidebar will open by default on changelist views
    "DONT_SUPPORT_ME": False,  # Hide github link in sidebar footer
    "SIDEBAR_FOOTNOTE": "",  # add footnote to sidebar
    "APPS_REORDER": {
        # Custom configurations for third-party apps that can't be modified directly in their `apps.py`
        "auth": {
            "icon": "fa-solid fa-person-military-pointing",  # FontAwesome icon for the 'auth' app
            "name": "Authentication",  # Custom name for the 'auth' app
            "hide": False,  # Whether to hide the 'auth' app from the sidebar (set to True to hide)
            "divider_title": "Auth",  # Divider title for the 'auth' section
        },
    },
}
