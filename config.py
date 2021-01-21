import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    S3_BUCKET = os.environ.get('BUCKET_NAME')
    S3_KEY = os.environ.get('AWS_KEY')
    S3_SECRETKEY = os.environ.get('AWS_SECRET_KEY')
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    BT_MERCHANTKEY=os.environ.get('BRAINTREE_MERCHANTKEY')
    BT_PUBLICKEY=os.environ.get('BRAINTREE_PUBLICKEY')
    BT_PRIVATEKEY=os.environ.get('BRAINTREE_PRIVATEKEY')
    GOOGLE_CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET=os.environ.get("GOOGLE_CLIENT_SECRET")


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
