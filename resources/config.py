import os, secrets

class Config:
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Scissor REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")
    JWT_SECRET_KEY = secrets.token_hex(32)
    
    DEFAULT_SERVER =  'http://127.0.0.1:5000/'