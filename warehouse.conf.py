# Warehouse Configuration
import os
import twelve
import urlparse

config = twelve.Configuration(adapter="django")

DEBUG = False

CONF_ROOT = os.path.dirname(__file__)

DATABASES = config.databases

DATABASES["default"]["ENGINE"] = "django_hstore.postgresql_psycopg2"

if "REDIS_URL" in os.environ:
    redis_url = os.environ["REDIS_URL"]
elif "OPENREDIS_URL" in os.environ:
    redis_url = os.environ["OPENREDIS_URL"]
elif "REDISTOGO_URL" in os.environ:
    redis_url = os.environ["REDISTOGO_URL"]
else:
    redis_url = "redis://localhost:6379/"

parsed_redis_url = urlparse.urlparse(redis_url)

REDIS_HOST = parsed_redis_url.hostname
REDIS_PORT = int(parsed_redis_url.port)
REDIS_PASSWORD = parsed_redis_url.password

RQ_REDIS_HOST = REDIS_HOST
RQ_REDIS_PORT = REDIS_PORT
RQ_REDIS_PASSWORD = REDIS_PASSWORD
RQ_REDIS_DB = 1

PYPI_REDIS_DATABASE = 2

SOUTH_DATABASE_ADAPTERS = {
    "default": "south.db.postgresql_psycopg2",
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
            "format": "[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s",
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
}

if config.disable_warehouse_api_history:
    WAREHOUSE_API_HISTORY = False

WAREHOUSE_SYNC_USERS = ["PyPI"]

WAREHOUSE_DOWNLOAD_SOURCES = {
    "PyPI": "warehouse.downloads.pypi",
}
