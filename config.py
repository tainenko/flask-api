import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False


class DevelopmentCOnfig(BaseConfig):
    CONFIG_NAME = 'dev'
    SECRET_KEY = os.getenv("DEV_SECRET_KEY")
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    CONFIG_NAME = 'test'
    CONFIG_SECRET_KEY = os.getenv("TEST_SECRET_KEY")
    DEBUG = True
    TESTING = True
    SQLACHEMY_DATABAE_URI = f"sqlite:///{basedir}/tests/app-test.db"


class ProductionConfig(BaseConfig):
    CONFIG_NAME = 'prod'
    CONFIG_SECRET_KEY = os.getenv("PROD_SECRET_KEY")
    DEBUG = False
    TESTING = False


configs = [DevelopmentCOnfig, TestingConfig, ProductionConfig]
config_map = {cfg.CONFIG_NAME: cfg for cfg in configs}
