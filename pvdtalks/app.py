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
from .config import config_app, config_celery
from .extensions import register_extensions
from .views import blueprint

from .tasks import celery


def create_app() -> Flask:
  app = Flask(__name__)
  config_app(app)

  # Setup the CLI
  register_cli(app)

  # Register extensions
  register_extensions(app)

  # Register routes
  app.register_blueprint(blueprint)

  config_celery(celery)

  TaskBase = celery.Task
  class ContextTask(TaskBase):
    def __call__(self, *args, **kwargs):
      with app.app_context():
        return TaskBase.__call__(self, *args, **kwargs) 
  celery.Task = ContextTask

  return app, celery
