import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Default configurations.
    Loads default environmental variables
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    GITHUB_ROOT_URL = os.getenv('GITHUB_ROOT_URL')


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = False
    DEBUG = True


configuration = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'development': DevelopmentConfig
}
