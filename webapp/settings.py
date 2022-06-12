import os

from icecream import install

install()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from my_secrets import secrets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.SECRET_KEY
SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "application",
    "users",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "django_extensions",
    "storages",
    "django_quill",
    "django_secrets",
    # adding django-agents to the installed apps
    "django_user_agents",
]

AUTH_USER_MODEL = "users.User"

# Adding Cache Backend for django-user-agents for rapid parsing
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': 'http://127.0.0.1:8000/',
#     }
# }

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = "default"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # middleware for django-agents
    "django_user_agents.middleware.UserAgentMiddleware",
]

ROOT_URLCONF = "webapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "application.context_processors.aws_media",
            ],
        },
    },
]

WSGI_APPLICATION = "webapp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    # 'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True
USE_L10N = True
USE_TZ = False

LANGUAGES = (('de', 'de'),)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/signin/"
LOGIN_REDIRECT_URL = "/"

BOOTSTRAP5 = {
    "error_css_class": "django_bootstrap5-error",
    "required_css_class": "django_bootstrap5-required",
    "javascript_in_head": True,
    "layout": "floating",
}

# --------------- static files configuration for development ------------------#
# static files configuration for development
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static') ]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# --------------------- media files configuration for development-----------------#
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -------------------------AWS S3 CONFIGURATION---------------------------#
AWS_ACCESS_KEY_ID = secrets.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = secrets.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = secrets.AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_DEFAULT_ACL = secrets.AWS_DEFAULT_ACL
AWS_S3_REGION_NAME = "us-east-1"

# --------------- static files configuration for production ------------------#
# AWS_LOCATION = 'static'
STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# --------------------- media files configuration for production-----------------#
MEDIA_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "webapp.storages.MediaStore"


PRIVATE_MEDIA_LOCATION = "private"
PRIVATE_FILE_STORAGE = "webapp.storages.PrivateMediaStorage"

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Kurs Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Admin",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Admin",
    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "books/img/logo.png",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the library",
    # Copyright on the footer
    "copyright": "Anna Holfeld",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "auth.User",
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # model admin to link to (Permissions checked against model)
        {"model": "users.User"},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {
            "name": "Support",
            "url": "https://github.com/farridav/django-jazzmin/issues",
            "new_window": True,
        },
        {"model": "users.user"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [
        "Sites",
        "auth",
    ],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": ["application.Completed", "application.access"],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "application.training",
        "application.module",
        "application.media",
        "application.page",
    ],
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "users.user": "fas fa-users-cog",
        "application.training": "fas fa-solid fa-rocket",
        "application.module": "fas fa-solid fa-book",
        "application.media": "fas fa-bookmark",
        "application.page": "far fa-file-alt",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_css": "assets/css/admin.css",
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    # "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

# Quill
QUILL_CONFIGS = {
    "default": {
        "theme": "snow",
        "modules": {
            "syntax": True,
            "toolbar": [
                [{'header': 1}, {'header': 2}],
                ['bold', 'italic', 'underline', 'strike', {"color": []}, {"align": []}],
                [{'list': 'ordered'}, {'list': 'bullet'}],
                ['clean'],
            ],
        },
    },
}
