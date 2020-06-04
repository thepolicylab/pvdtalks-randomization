from pathlib import Path
from typing import (Union, List)

from flask import (Blueprint, abort, current_app, flash, redirect, render_template,
  request, send_from_directory, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from .extensions import lm
from .models import Submission, User, db
from . import tasks

import numpy as np
import pandas as pd


blueprint = Blueprint('public', __name__, template_folder='templates')


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


@blueprint.route('/')
def index_route():
  return render_template('index.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login_route():
  if current_user.is_authenticated:
    flash('You are already logged in')
    return redirect(url_for('public.index_route'))
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
    return redirect(url_for('public.index_route'))

  flash('Incorrect password')
  return render_template('login.html')


@blueprint.route('/logout')
@login_required
def logout_route():
  logout_user()
  return redirect(url_for('public.index_route'))


def get_url_from_submission(submission: Submission) -> str:
  return url_for('public.download_file', file_id=submission.id, final_filename=submission.final_filename)


@blueprint.route('/download/<int:file_id>/<final_filename>')
@login_required
def download_file(file_id: int, final_filename: str):
  submission = Submission.query.get(file_id)
  if not submission:
    return abort(404)

  # Do you have permission to download?
  if (not current_user.is_lab_member) or (submission.user_id != current_user.id):
    return abort(401)

  # Did you get this URL from the right place?
  if not submission.final_filename == final_filename:
    return abort(404)

  # If so, then you should be able to download this file
  return send_from_directory(
    get_path_from_filename(submission.original_filename, create=False),
    submission.final_filename
  )


@blueprint.route('/foo')
def foo_route():
  s = tasks.long_add.delay(20, 30)
  return 'asdf'


@blueprint.route('/download')
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
  base_dir = Path(current_app.config['UPLOAD_DIR'])

  if create and not base_dir.exists():
    base_dir.mkdir()

  return base_dir


@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_route():
  if request.method == 'GET':
    return render_template('upload.html')

  if request.content_length > current_app.config['UPLOAD_MAX_SIZE']:
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
  ## (jwb): This is probably very inefficient but perhaps a reasonable place to start.
  def complete_ra(N:int,m:int,conditions:List[int]) -> pd.Series:
      assignment = np.random.permutation(np.repeat(conditions,[N-m,m],axis=0))
      return assignment

  N = len(cur_savename)
  m = np.floor(N/2)
  cur_savename = cur_savename.assign(trt=complete_ra(N=N,m=m,conditions=[0,1]))

  ## Make sure that dat2 is the same number of rows as dat
  assert(len(dat2)==len(dat))
  ## Make sure that we have randomly assigned half to treatment
  assert(sum(dat2['trt'])==np.floor(len(dat)/2))

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
  return redirect(url_for('public.index_route'))
