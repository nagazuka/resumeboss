import os
import tenjin

from tenjin.helpers import *

engine = tenjin.Engine(path=['template'])

def render(dir, context):
  tex = engine.render('designers-cv-template.tex', context)
  print(tex)
  file = open(os.path.join(dir,'designers-cv-template-rendered.tex'), 'w')
  file.write(tex)
  file.close()

if __name__ == "__main__":
    context = {
      'name': 'Shanny Anoep',
      'headline': '',
      'summary': ''
    }
    dir = 'output'
    render(dir, context)
    render(dir, context)
