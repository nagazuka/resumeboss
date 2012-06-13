import shutil
import subprocess
import tempfile
import os
import time
import render
import transform
from settings import * 

resume_prefix = 'cv-template-rendered'

def execute_latex(tempdir):
  print("Executing latex")
  subprocess.call([PDFLATEX,template_path(tempdir)], cwd=tempdir)

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

def photo_paths(dir):
  photo_path1 = os.path.join(dir,'photo.pdf')
  photo_path2 = os.path.join(dir,'picture.jpg')
  return [photo_path1, photo_path2]

def download_path():
  download_dir = '/var/www/vhosts/nagazuka.nl/httpdocs/resumeboss/download/'
  unique = str(int(time.time()))
  resume_file = 'resume_' + unique + '.pdf';
  resume_path = os.path.join(download_dir,resume_file)
  return resume_path, resume_file

def copy_template(tempdir):
  for photo_path in photo_paths(TEMPLATE_DIR):
    shutil.copy(photo_path, tempdir)

def delete_tempdir(dir):
  shutil.rmtree(dir)

def transform_profile(profile):
  return transform.transform_linkedin(profile)

def generate(profile, template_name, callback):

  tempdir = create_tempdir()
  print("tempdir: %s" % tempdir)

  context = transform_profile(profile) 
  render_template(tempdir, context, template_name)

  copy_template(tempdir)
  execute_latex(tempdir)

  download_file = copy_resume(tempdir)
  delete_tempdir(tempdir)

  print("download_file: %s" % download_file)
  callback(download_file)
