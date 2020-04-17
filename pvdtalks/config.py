import os

from celery import Celery
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def config_app(app: Flask):
  app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'])

  app.config['UPLOAD_DIR'] = os.environ['UPLOAD_DIR']
  app.config['UPLOAD_MAX_SIZE'] = int(os.environ['UPLOAD_MAX_SIZE'])


def config_celery(celery_app: Celery):
  celery_app.conf.update({
    'broker_url': os.environ['CELERY_BROKER'],
    'imports': ('pvdtalks.tasks', ),
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
  })