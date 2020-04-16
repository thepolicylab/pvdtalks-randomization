from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
lm = LoginManager()


def register_extensions(app: Flask):
  db.init_app(app)
  lm.init_app(app)