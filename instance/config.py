import os

class Config:
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class StagingConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    TESTING = False

app_config = {
    'DEVELOPMENT': DevelopmentConfig,
    'TESTING': TestingConfig,
    'STAGING': StagingConfig,
    'PRODUCTION': ProductionConfig,
}