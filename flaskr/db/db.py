from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import CommonSettings

settings = CommonSettings()

db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB.DSN
    db.init_app(app)
