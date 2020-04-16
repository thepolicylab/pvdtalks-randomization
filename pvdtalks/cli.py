import getpass

import click
from flask import Flask
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

from .models import User, db


user_cli = AppGroup('user')
db_cli = AppGroup('db')


@db_cli.command('create')
def create_db_command():
  db.create_all()


@user_cli.command('create')
@click.argument('email')
@click.option('-l', '--lab', 'is_lab_member', is_flag=True)
def create_user_command(email: str, is_lab_member: bool):
  click.echo(f'Creating user {email}')
  email = email.strip().lower()

  user = User.query.filter_by(email=email).first()
  if user:
    click.echo(f'User {email} already exists. Perhaps you want to reset the password?')
    return

  password = getpass.getpass('Password: ')
  check_password = getpass.getpass('Retype password: ')
  while password != check_password:
    click.echo('Passwords don\'t match. Try again.')
    password = getpass.getpass('Password: ')
    check_password = getpass.getpass('Retype password: ')
  user = User(email=email, password=generate_password_hash(password), is_lab_member=is_lab_member)
  db.session.add(user)
  db.session.commit()


def register_cli(app: Flask):
  app.cli.add_command(user_cli)
  app.cli.add_command(db_cli)