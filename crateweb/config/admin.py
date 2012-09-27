from warehouse.settings.base import AdminSettings

from crateweb.config import base as config


class Development(config.Development, AdminSettings):
    """
    Development settings for crate.io
    """


class Production(config.Production, AdminSettings):
    """
    Production settings for crate.io
    """
