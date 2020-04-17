#!/bin/bash

export FLASK_APP=autoapp.py

export SECRET_KEY=aasfawoieufhaweiuhfausidhfad

export SQLALCHEMY_DATABASE_URI=sqlite:////Users/kwilso14/repo/brown/pvdtalks-randomization/db.db
export SQLALCHEMY_TRACK_MODIFICATIONS=False

export UPLOAD_DIR=/Users/kwilso14/repo/brown/pvdtalks-randomization/uploads
export UPLOAD_MAX_SIZE=1000000

export RABBITMQ_DEFAULT_USER=user
export RABBITMQ_DEFAULT_PASS=password

export CELERY_BROKER=amqp://user:password@127.0.0.1:5672
export FLOWER_BROKER=amqp://user:password@127.0.0.1:5672

flask run
