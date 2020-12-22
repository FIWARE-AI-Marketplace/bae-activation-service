import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False

    # Marketplace Keyrock
    BAE_KEYROCK_SERVER = os.getenv('BAE_KEYROCK_SERVER')
    BAE_KEYROCK_APPID = os.getenv('BAE_KEYROCK_APPID')
    BAE_KEYROCK_USERNAME = os.getenv('BAE_KEYROCK_USERNAME')
    BAE_KEYROCK_PASSWORD = os.getenv('BAE_KEYROCK_PASSWORD')

    # Provider Keyrock
    PROVIDER_KEYROCK_SERVER = os.getenv('PROVIDER_KEYROCK_SERVER')
    PROVIDER_KEYROCK_APPID = os.getenv('PROVIDER_KEYROCK_APPID')
    PROVIDER_KEYROCK_USERNAME = os.getenv('PROVIDER_KEYROCK_USERNAME')
    PROVIDER_KEYROCK_PASSWORD = os.getenv('PROVIDER_KEYROCK_PASSWORD')

    # Provider API Umbrella
    PROVIDER_UMBRELLA_SERVER = os.getenv('PROVIDER_UMBRELLA_SERVER')
    PROVIDER_UMBRELLA_ADMIN_TOKEN = os.getenv('PROVIDER_UMBRELLA_ADMIN_TOKEN')
    PROVIDER_UMBRELLA_API_KEY = os.getenv('PROVIDER_UMBRELLA_API_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

