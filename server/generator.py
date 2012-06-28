import shutil
import urllib
import logging
import subprocess
import tempfile
import os
import time
import render
import transform
from settings import * 

resume_prefix = 'cv-template-rendered'
interaction_mode = '-interaction=nonstopmode'

def execute_latex(tempdir):
  logging.info("Executing latex")
  subprocess.call([PDFLATEX, interaction_mode, template_path(tempdir)], cwd=tempdir)

def copy_resume(tempdir):
  path, download_file = download_path() 
  shutil.copy(resume_path(tempdir), path)
  return download_file

def render_template(tempdir, context, template_name):
  render.render(template_name, template_path(tempdir), context)

def create_tempdir():
  tempdir = tempfile.mkdtemp(prefix='template')
  return tempdir

def resume_path(dir):
  resume_path = os.path.join(dir,resume_prefix + '.pdf')
  return resume_path

def template_path(dir):
  template_path = os.path.join(dir,resume_prefix +'.tex')
  return template_path

def photo_path(dir):
  return os.path.join(dir,'picture.jpg')

def download_path():
  download_dir = '/var/www/vhosts/nagazuka.nl/httpdocs/resumeboss/download/'
  unique = str(int(time.time()))
  resume_file = 'resume_' + unique + '.pdf';
  resume_path = os.path.join(download_dir,resume_file)
  return resume_path, resume_file

def delete_tempdir(dir):
  shutil.rmtree(dir)

def transform_profile(profile):
  return transform.transform_linkedin(profile)

def retrieve_picture(profile, tempdir):
  if 'pictureUrl' in profile:
    picture_url = profile['pictureUrl']
    picture_path = photo_path(tempdir)
    urllib.urlretrieve(picture_url, picture_path) 

def generate(profile, template_name, callback):
  tempdir = create_tempdir()
  logging.info("tempdir: %s" % tempdir)

  context = transform_profile(profile) 
  retrieve_picture(profile, tempdir)
  render_template(tempdir, context, template_name)

  execute_latex(tempdir)

  download_file = copy_resume(tempdir)

  if not DEBUG:
    delete_tempdir(tempdir)

  logging.info("download_file: %s" % download_file)
  callback(download_file)
