from itertools import izip

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

def transform_dates(position):
    if not 'startDate' in position: 
      startDate = ''
    else:
      startDate = position['startDate']['year']

    if 'isCurrent' in position and (position['isCurrent'] == 'true' or position['isCurrent'] == True):
      endDate = 'present'
    elif 'endDate' in position: 
      endDate = position['endDate']['year']
    else:
      endDate = ''

    return "%s - %s" % (startDate, endDate)

def sanitize_object(dictionary, key):
    if not key in dictionary or len(dictionary[key]) == 0:
      dictionary[key] = ' '
    else:
      dictionary[key] = dictionary[key].replace('\n',r'\\')
      for special_char in ['&','%','$','_','^','#','~','{','}']:
        dictionary[key] = dictionary[key].replace(special_char,'\\' + special_char)

def transform_linkedin(profile):
  print("transforming %s" % profile)
  for key, value in profile.iteritems() :
    print key, value

  firstName = profile['firstName']
  lastName = profile['lastName']
  name = firstName + ' ' + lastName
  headline = profile['headline']
  if ('summary' in profile):
    summary = profile['summary']
  else:
    summary = ''
  positions = profile['positions']['values']
  educations = profile['educations']['values']
  if ('certifications' in profile):
    certifications = profile['certifications']['values']
  else:
    certifications = []
  skills = profile['skills']['values']
  
  paired_skills = []
  for skill1, skill2 in pairwise(skills):
    paired_skills.append( (skill1, skill2) ) 

  for position in positions:
    position['period'] = transform_dates(position)    
    sanitize_object(position, 'summary')

  for education in educations:
    education['period'] = transform_dates(education)
    sanitize_object(education, 'notes')
   
  context = {}
  context['name'] = name
  context['firstName'] = firstName
  context['lastName'] = lastName
  context['headline'] = headline
  context['summary'] = summary
  context['positions'] = positions
  context['educations'] = educations
  context['certifications'] = certifications
  context['skills'] = paired_skills

  return context
