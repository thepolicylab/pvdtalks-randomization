import datetime

from flask_login import UserMixin

from .extensions import db


class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64), nullable=False, unique=True)
  password = db.Column(db.String(200), nullable=False)
  is_lab_member = db.Column(db.Boolean, nullable=False, default=False)


class Submission(db.Model):
  __tablename__ = 'submissions'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
  original_filename = db.Column(db.String(256), nullable=False)
  final_filename = db.Column(db.String(256), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Answer(db.Model):
  __tablename__ = 'answers'

  id = db.Column(db.Integer, primary_key=True)
  answer = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
