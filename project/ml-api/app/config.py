import os

class BaseConfig:
    APP_NAME = os.getenv("APP_NAME", "ml-api")
    SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
    RESTX_MASK_SWAGGER = False
    ERROR_404_HELP = False
    MODEL_PATH = os.getenv("MODEL_PATH", "models/titanic_clf.joblib")
    MODEL_METADATA = os.getenv("MODEL_METADATA", "models/metadata.json")
    print(f"🔖 Usando modelo en: {MODEL_PATH}" )
    print(f"📝 Usando metadata en: {MODEL_METADATA}" )

class DevConfig(BaseConfig):
    DEBUG = True

class ProdConfig(BaseConfig):
    DEBUG = False

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return DevConfig if env == "development" else ProdConfig