import shutil
import subprocess
import tempfile
import os
import time

def execute_latex(tempdir):
  subprocess.call(['pdflatex',template_path(tempdir)], cwd=tempdir)
  #process = subprocess.Popen(['pdflatex',template_path(tempdir)], cwd=tempdir)
  #process.wait()

def copy_resume(tempdir):
  path, download_file = download_path() 
  shutil.copy(resume_path(tempdir), path)
  return download_file

def render_template(tempdir):
  return None

def create_tempdir():
  tempdir = tempfile.mkdtemp(prefix='template')
  return tempdir

def resume_path(dir):
  template_path = os.path.join(dir,'designers-cv.pdf')
  return template_path

def template_path(dir):
  template_path = os.path.join(dir,'designers-cv.tex')
  return template_path

def photo_path(dir):
  photo_path = os.path.join(dir,'photo.pdf')
  return photo_path

def download_path():
  download_dir = '/var/www/vhosts/nagazuka.nl/httpdocs/resumeboss/download/'
  unique = str(int(time.time()))
  resume_file = 'resume_' + unique + '.pdf';
  resume_path = os.path.join(download_dir,resume_file)
  return resume_path, resume_file

def copy_template(tempdir):
  basedir = 'template'
  shutil.copy(template_path(basedir), tempdir)
  shutil.copy(photo_path(basedir), tempdir)

def delete_tempdir(dir):
  shutil.rmtree(dir)

def generate():
  tempdir = create_tempdir()
  print("tempdir: %s" % tempdir)
  copy_template(tempdir)
  render_template(tempdir)
  execute_latex(tempdir)
  download_file = copy_resume(tempdir)
  delete_tempdir(tempdir)
  print("download_file: %s" % download_file)
  return download_file

if __name__ == "__main__":
    generate()
    generate()
