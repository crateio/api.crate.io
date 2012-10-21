from warehouse.settings.base import WebSettings

from crateweb.config import base as config


class Development(config.Development, WebSettings):
    """
    Development settings for crate.io
    """


class Production(config.Production, WebSettings):
    """
    Production settings for crate.io
    """
