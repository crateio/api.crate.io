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
