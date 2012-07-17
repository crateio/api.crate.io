# Warehouse Configuration
import os
import twelve

config = twelve.Configuration(adapter="django")

DEBUG = True
TASTYPIE_FULL_DEBUG = True

CONF_ROOT = os.path.dirname(__file__)

DATABASES = config.databases

DATABASES["default"]["ENGINE"] = "django_hstore.postgresql_psycopg2"

SOUTH_DATABASE_ADAPTERS = {
    "default": "south.db.postgresql_psycopg2",
}

SECRET_KEY = config.secret_key

if "default" in config.emails:
    for k, v in config.emails["default"].items():
        globals()["EMAIL_%s" % k] = v


STATIC_URL = "https://dtl9zya2lik3.cloudfront.net/"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"

AWS_ACCESS_KEY_ID = config.aws_access_key_id
AWS_SECRET_ACCESS_KEY = config.aws_secret_access_key
AWS_STORAGE_BUCKET_NAME = config.aws_storage_bucket_name

AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False

AWS_HEADERS = {
    "Cache-Control": "max-age=31556926",
}
