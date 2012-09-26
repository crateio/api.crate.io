from warehouse.settings.base import ApiSettings

from crateweb.config import base as config


class Development(config.Development, ApiSettings):
    """
    Development settings for api.crate.io
    """


class Production(config.Production, ApiSettings):
    """
    Production settings for api.crate.io
    """
