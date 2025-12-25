from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ljdoces.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["WHATSAPP_LJ"] = "11962819619"

    db.init_app(app)

    from . import routes, models
    routes.init_app(app)

    return app