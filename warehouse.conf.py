# Warehouse Configuration
import os
import twelve

config = twelve.Configuration(adapter="django")

import dj_database_url
import dj_redis_url


DEBUG = False

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    "default": dj_database_url.config(default="postgres://localhost"),
}

DATABASES["default"]["ENGINE"] = "django_hstore.postgresql_psycopg2"

SOUTH_DATABASE_ADAPTERS = {
    "default": "south.db.postgresql_psycopg2",
}

REDIS = {
    "default": dj_redis_url(default="redis://localhost", db=0),
    "rq": dj_redis_url(default="redis://localhost", db=1),
    "pypi": dj_redis_url(default="redis://localhost", db=2),
}

EXTRA_INSTALLED_APPS = [
    "djangosecure",
]

EXTRA_MIDDLEWARE_CLASSES = [
    "djangosecure.middleware.SecurityMiddleware",
]

if "default" in config.emails:
    for k, v in config.emails["default"].items():
        globals()["EMAIL_%s" % k] = v

SECRET_KEY = config.secret_key

STATIC_URL = "https://dtl9zya2lik3.cloudfront.net/"

#DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
DEFAULT_FILE_STORAGE = "fixed_storage.FixedS3BotoStorage"

AWS_ACCESS_KEY_ID = config.aws_access_key_id
AWS_SECRET_ACCESS_KEY = config.aws_secret_access_key
AWS_STORAGE_BUCKET_NAME = config.aws_storage_bucket_name

if config.aws_s3_custom_domain:
    AWS_S3_CUSTOM_DOMAIN = config.aws_s3_custom_domain

AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False

AWS_HEADERS = {
    "Cache-Control": "max-age=31556926",
}

WAREHOUSE_PACKAGE_BASE_DIR = "dists"
WAREHOUSE_PACKAGE_PATH_HASH = "sha256"
WAREHOUSE_DIGEST_TYPES = ["md5", "sha256"]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 31557600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,

    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s]  %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },

    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "sentry": {
            "level": "ERROR",
            "class": "raven.handlers.logging.SentryHandler",
        },
    },

    "root": {
        "handlers": ["console", "sentry"],
        "level": "DEBUG",
    },

    "loggers": {
        "requests.packages.urllib3": {
            "handlers": [],
            "propagate": False,
        },
    },
}

if config.disable_warehouse_api_history:
    WAREHOUSE_API_HISTORY = False

WAREHOUSE_SYNC_USERS = ["PyPI"]

WAREHOUSE_DOWNLOAD_SOURCES = {
    "PyPI": "warehouse.downloads.pypi",
}
