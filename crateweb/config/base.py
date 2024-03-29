import os

import dj_database_url
import dj_redis_url
import dj_search_url


class Settings(object):
    CONF_ROOT = os.path.dirname(os.path.abspath(__file__))

    DATABASES = {"default": dj_database_url.config(default="postgres://localhost/warehouse")}

    REDIS = dj_redis_url.config(default="redis://localhost", db=0)

    CACHES = {
        "default": {
            "BACKEND": "redis_cache.RedisCache",
            "LOCATION": "%s:%s" % (REDIS["HOST"], REDIS["PORT"]),
            "OPTIONS": {
                "DB": REDIS["DB"],
                "PASSWORD": REDIS["PASSWORD"],
            },
        },
    }

    HAYSTACK_CONNECTIONS = {"default": dj_search_url.config(default="elasticsearch://localhost:9200/api.crate.io")}

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

    LOGGING = {
        "handlers": {
            "sentry": {
                "level": "ERROR",
                "class": "raven.handlers.logging.SentryHandler",
            },
        },
        "root": {
            "handlers": ["console", "sentry"],
        },
        "loggers": {
            "boto": {
                "handlers": ["sentry"],
                "propagate": False,
            },
            "newrelic.lib.requests.packages.urllib3": {
                "handlers": ["sentry"],
                "propagate": False,
            },
            "pyelasticsearch": {
                "handlers": ["sentry"],
                "propagate": False,
            }
        },
    }

    WAREHOUSE_ALWAYS_MODIFIED_NOW = False
    WAREHOUSE_DIGEST_TYPES = ["md5", "sha256"]
    WAREHOUSE_PACKAGE_BASE_DIR = "dists"
    WAREHOUSE_PACKAGE_PATH_HASH = "sha256"
    WAREHOUSE_SYNC_USERS = ["PyPI"]

    WAREHOUSE_DOWNLOAD_COUNT_TIMEOUT = 120 * 60
    WAREHOUSE_DOWNLOAD_SOURCES = {
        "PyPI": "warehouse.downloads.pypi.downloads",
    }

    if "WAREHOUSE_API_HISTORY" in os.environ:
        WAREHOUSE_API_HISTORY = bool(int(os.environ.get("WAREHOUSE_API_HISTORY", 1)))

    if "WAREHOUSE_UPDATE_DOWNLOAD_COUNTS" in os.environ:
        WAREHOUSE_UPDATE_DOWNLOAD_COUNTS = bool(int(os.environ.get("WAREHOUSE_UPDATE_DOWNLOAD_COUNTS", 1)))


class Development(Settings):
    DEBUG = True

    STATIC_ROOT = os.path.join(Settings.CONF_ROOT, "site_media", "static")
    STATIC_URL = "/site_media/static/"

    MEDIA_ROOT = os.path.join(Settings.CONF_ROOT, "site_media", "media")
    MEDIA_URL = "/site_media/media/"

    INSTALLED_APPS = [
        "devserver",
    ]

    DEVSERVER_MODULES = [
        "devserver.modules.sql.SQLRealTimeModule",
        "devserver.modules.sql.SQLSummaryModule",
        "devserver.modules.profile.ProfileSummaryModule",
        "devserver.modules.cache.CacheSummaryModule",
        #"devserver.modules.profile.LineProfilerModule",
    ]

    DEVSERVER_AUTO_PROFILE = True


class Production(Settings):
    DEBUG = False

    MIDDLEWARE = [
        (0, "djangosecure.middleware.SecurityMiddleware"),
    ]

    DEFAULT_FILE_STORAGE = "crateweb.storage.FixedS3BotoStorage"

    STATICFILES_STORAGE = "crateweb.storage.CachedS3BotoStaticFileStorage"
    STATICFILES_DOMAIN = os.environ.get("STATICFILES_DOMAIN", None)

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
