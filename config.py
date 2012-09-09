from warehouse.settings.base import WarehouseSettings

import os

import dj_database_url
import dj_redis_url


class Settings(WarehouseSettings):
    CONF_ROOT = os.path.dirname(os.path.abspath(__file__))

    DATABASES = {"default": dj_database_url.config(default="postgres://localhost")}
    DATABASES["default"]["ENGINE"] = "django_hstore.postgresql_psycopg2"
    SOUTH_DATABASE_ADAPTERS = {"default": "south.db.postgresql_psycopg2"}

    REDIS = {
        "default": dj_redis_url.config(default="redis://localhost", db=0),
        "rq": dj_redis_url.config(default="redis://localhost", db=1),
        "pypi": dj_redis_url.config(default="redis://localhost", db=2),
    }

    CACHES = {
        "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": "%s:%s" % (REDIS["default"]["HOST"], REDIS["default"]["PORT"]),
            "OPTIONS": {
                "DB": REDIS["default"]["DB"],
                "PASSWORD": REDIS["default"]["PASSWORD"],
            },
        },
    }

    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.BCryptPasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
        "django.contrib.auth.hashers.SHA1PasswordHasher",
        "django.contrib.auth.hashers.MD5PasswordHasher",
        "django.contrib.auth.hashers.CryptPasswordHasher",
    ]

    SECRET_KEY = os.environ["SECRET_KEY"]

    SESSION_COOKIE_HTTPONLY = True

    SECURE_FRAME_DENY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

    LOGGING = WarehouseSettings.LOGGING
    LOGGING["handlers"]["sentry"] = {"level": "ERROR", "class": "raven.handlers.logging.SentryHandler"}
    LOGGING["root"]["handlers"] += ["sentry"]
    LOGGING["loggers"]["newrelic.lib.requests.packages.urllib3"] = {"handlers": [], "propagate": False}

    WAREHOUSE_ALWAYS_MODIFIED_NOW = False
    WAREHOUSE_API_HISTORY = os.environ.get("DISABLE_WAREHOUSE_API_HISTORY", False)
    WAREHOUSE_DIGEST_TYPES = ["md5", "sha256"]
    WAREHOUSE_PACKAGE_BASE_DIR = "dists"
    WAREHOUSE_PACKAGE_PATH_HASH = "sha256"
    WAREHOUSE_SYNC_USERS = ["PyPI"]

    WAREHOUSE_DOWNLOAD_COUNT_TIMEOUT = 120 * 60
    WAREHOUSE_DOWNLOAD_SOURCES = {
        "PyPI": "warehouse.downloads.pypi.downloads",
    }


class Development(Settings):
    DEBUG = True

    STATIC_ROOT = os.path.join(Settings.CONF_ROOT, "site_media", "static")
    STATIC_URL = "/site_media/static/"

    MEDIA_ROOT = os.path.join(Settings.CONF_ROOT, "site_media", "media")
    MEDIA_URL = "/site_media/media/"


class Production(Settings):
    DEBUG = False

    MIDDLEWARE_CLASSES = ["djangosecure.middleware.SecurityMiddleware"] + WarehouseSettings.MIDDLEWARE_CLASSES

    DEFAULT_FILE_STORAGE = "fixed_storage.FixedS3BotoStorage"

    STATICFILES_STORAGE = "fixed_storage.CachedS3BotoStaticFileStorage"

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SECURE_URLS = False
    AWS_HEADERS = {"Cache-Control": "max-age=31556926"}

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    SESSION_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31557600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
