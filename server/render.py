import tenjin
from settings import *
from tenjin.helpers import *

engine = tenjin.Engine(path=[TEMPLATE_DIR])
#engine = tenjin.Engine(path=['/home/development/resumeboss/template'])

def render(template_name, output_path, context):
  tex = engine.render(template_name + '-template.tex', context)
  print(tex)
  file = open(output_path, 'w')
  file.write(tex)
  file.close()

if __name__ == "__main__":
    context = {
      'name': 'Shanny Anoep',
      'headline': '',
      'summary': '',
      'positions': []
    }
    dir = 'output/designers-cv-template-rendered.tex'
    dir2 = 'output/plain-cv-template-rendered.tex'
    render('designers-cv', dir, context)
    render('plain-cv', dir2, context)
