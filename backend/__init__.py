from flask import Flask
from backend.config import Config
from backend.extensions import db, migrate, api
from backend import views


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    api.register_blueprint(views.blp)

    return app