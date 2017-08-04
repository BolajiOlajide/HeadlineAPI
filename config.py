"""
Configuration settings for the Headline API.

The definition of the different configuration settings is contained here:
- Development Configuration
- Production Configuration
- Testing Configuration
"""

import dotenv

dotenv.load()


class Config:
    """
    The definition of the global configuration is defined here.
    Attributes such as SECRET_KEY are the same no matter the platform used.
    """

    SECRET_KEY = dotenv.get("SECRET_KEY")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_TOKEN_AUTH = True
    DEBUG = False
    SSLIFY_SUBDOMAINS = True
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100


class DevelopmentConfig(Config):
    """
    The configuration settings for development mode is defined here.
    Attributes such as SQLALCHEMY_DATABASE_URI, DEBUG are different for other
    modes, so they are defined in a class called DevelopmentConfig.
    """

    SQLALCHEMY_DATABASE_URI = dotenv.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class TestingConfig(Config):
    """
    The configuration settings for testing mode is defined here.
    Attributes such as SQLALCHEMY_DATABASE_URI, TESTING are different for other
    modes, so they are defined in a class called TestingConfig.
    """

    USE_RATE_LIMITS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = dotenv.get("TEST_DB")
    SERVER_NAME = dotenv.get("SERVER_NAME")


class ProductionConfig(Config):
    """
    The configuration settings for production mode is defined here.
    Attributes such as SQLALCHEMY_DATABASE_URI, DEBUG are different for other
    modes, so they are defined in a class called ProductionConfig.
    """

    SQLALCHEMY_DATABASE_URI = dotenv.get("DATABASE_URL")


# Object containing the different configuration classes.
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
