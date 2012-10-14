from warehouse.settings.base import AppSettings

from crateweb.config import base as config


class Development(config.Development, AppSettings):
    """
    Development settings for crate.io
    """


class Production(config.Production, AppSettings):
    """
    Production settings for crate.io
    """
