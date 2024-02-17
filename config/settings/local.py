from .base import *

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
    "django_browser_reload",
]

INTERNAL_IPS = ["127.0.0.1", "localhost"]

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

SECURE_SSL_REDIRECT = False

SECURE_HSTS_SECONDS = 0

SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda r: False,  # disables it
# }
