import os
import yaml

class Config(object):
    DEBUG = False
    TESTING = False

    with open(os.path.dirname(os.path.abspath(__file__)) + '/conf/blog.yaml') as f:
        config = yaml.load(f)

    BLOG_CONFIG = config


class DevConfig(Config):
    DEBUG = True
    TESTING = False


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

