import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", f"sqlite:///{os.path.join(base_dir, 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TITLE = "API for backend 2025 KPI course by Tsvetkov Vladyslav"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mega-secret-lab4-key")