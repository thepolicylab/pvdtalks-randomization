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


# TODO (khw): Get this setup with the 
with open('config.yml') as config_file:
  config = yaml.safe_load(config_file)


app = Flask(__name__)
app.config['SECRET_KEY'] = config['app']['secret_key']

user_cli = AppGroup('user')
app.cli.add_command(user_cli)

db_cli = AppGroup('db')
app.cli.add_command(db_cli)

app.config['SQLALCHEMY_DATABASE_URI'] = config['db']['uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['db'].get('track_modifications', False)
db = SQLAlchemy(app)

lm = LoginManager(app)

app.config['UPLOAD_DIR'] = config['uploads']['dir']
app.config['UPLOAD_MAX_SIZE'] = config['uploads']['max_size']


@lm.user_loader
def load_user(user_id: Union[str, int]):
  """
  Load a user from the database based on their id

  Args:
    user_id: The user to load

  Returns:
    User: The user
  """
  return User.query.get(int(user_id))



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


@app.route('/')
def index_route():
  return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_route():
  if current_user.is_authenticated:
    flash('You are already logged in')
    return redirect(url_for('index_route'))
  if request.method == 'GET':
    return render_template('login.html')
  email = request.form['email']
  password = request.form['password']

  user = User.query.filter_by(email=email).first()
  if not user:
    flash(f'No such user {email}')
    return render_template('login.html')
  
  if check_password_hash(user.password, password):
    login_user(user)
    return redirect(url_for('index_route'))
  
  flash('Incorrect password')
  return render_template('login.html')


@app.route('/logout')
@login_required
def logout_route():
  logout_user()
  return redirect(url_for('index_route'))


def get_url_from_submission(submission: Submission) -> str:
  return url_for('download_file', file_id=submission.id, final_filename=submission.final_filename)


@app.route('/download/<int:file_id>/<final_filename>')
@login_required
def download_file(file_id: int, final_filename: str):
  submission = Submission.query.get(file_id)

  # Do you have permission to download?
  if (not current_user.is_lab_member) or (submission.user_id != current_user.id):
    abort(401)
  
  # Did you get this URL from the right place?
  if not submission.final_filename == final_filename:
    abort(404)
  
  # If so, then you should be able to download this file
  return send_from_directory(
    get_path_from_filename(submission.original_filename, create=False),
    submission.final_filename
  )


@app.route('/download')
@login_required
def download_route():
  if current_user.is_lab_member:
    submissions = Submission.query.all()
  else:
    submissions = Submission.query.filter_by(user_id=current_user.id).all()
  
  files_urls_dates = []
  for submission in submissions:
    files_urls_dates.append((
      submission.original_filename,
      get_url_from_submission(submission),
      submission.created_at
    ))
  
  return render_template('download.html', files_urls_dates=files_urls_dates)


def get_path_from_filename(filename: str, create: bool = False) -> Path:
  """
  Return a full path for a file given its contents and its name.
  Note that for now this is just the base upload folder, but it really
  should be some sort of file hash or some such.

  Args:
    filename: The name of the file being saved
    create: Whether to created the upload directory when called
  
  Return:
    The path the file is contained in
  """
  base_dir = Path(app.config['UPLOAD_DIR'])

  if create and not base_dir.exists():
    base_dir.mkdir()

  return base_dir


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_route():
  if request.method == 'GET':
    return render_template('upload.html')
  
  if request.content_length > app.config['UPLOAD_MAX_SIZE']:
    flash('File too large')
    return render_template('upload.html')

  file = request.files.get('file')
  if not file or not file.filename:
    flash('No file selected')
    return render_template('upload.html')

  filename = secure_filename(file.filename)
  path = get_path_from_filename(filename, create=True)

  base_savename = path / filename

  # Make sure not to overwrite old files
  cur_savename = base_savename
  extension_num = 0
  while cur_savename.exists():
    cur_savename = cur_savename.with_suffix(f'.{extension_num}{cur_savename.suffix}')
    extension_num += 1

  #### TODO (khw): Here is where you could add your stuff Jake

  # Save the file
  file.save(cur_savename)

  # Make a note about who uploaded the file
  submision = Submission(
    user_id=current_user.id,
    original_filename=filename,
    final_filename=cur_savename.name
  )
  db.session.add(submision)
  db.session.commit()

  flash(f'File {filename} successfully uploaded')
  return redirect(url_for('index_route'))