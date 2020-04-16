import datetime
import getpass
from pathlib import Path
from typing import Union

import click
import yaml

from flask import Flask, abort, flash, send_from_directory, render_template, redirect, request, url_for
from flask.cli import AppGroup
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
  current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from . import models  # This registers all of our models
from .cli import register_cli
from .extensions import register_extensions
from .views import blueprint


def create_app() -> Flask:

  # TODO (khw): This is obviously bad
  with open('config.yml') as config_file:
    config = yaml.safe_load(config_file)

  app = Flask(__name__)

  app.config['SECRET_KEY'] = config['app']['secret_key']

  # Setup the CLI
  register_cli(app)

  # Configure the database
  app.config['SQLALCHEMY_DATABASE_URI'] = config['db']['uri']
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['db'].get('track_modifications', False)

  # Configure the uploader
  app.config['UPLOAD_DIR'] = config['uploads']['dir']
  app.config['UPLOAD_MAX_SIZE'] = config['uploads']['max_size']

  # Register extensions
  register_extensions(app)

  # Register routes
  app.register_blueprint(blueprint)

  return app
