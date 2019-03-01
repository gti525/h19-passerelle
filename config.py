import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgres://fpdgdsdmpfgcbv:e9475e3851180bed9881ead8f9ab1567bdefe60b6e144f3109f3a2c9dbeeff13@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d7077c2rlc150n"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgres://fpdgdsdmpfgcbv:e9475e3851180bed9881ead8f9ab1567bdefe60b6e144f3109f3a2c9dbeeff13@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d7077c2rlc150n"
