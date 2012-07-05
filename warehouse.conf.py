# Warehouse Configuration
import os
import twelve

config = twelve.Configuration(adapter="django")

DEBUG = True

CONF_ROOT = os.path.dirname(__file__)

DATABASES = config.databases

SECRET_KEY = config.secret_key

if "default" in config.emails:
    for k, v in config.emails["default"].items():
        globals()["EMAIL_%s" % k] = v
