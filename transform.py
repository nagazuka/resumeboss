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

    if not 'summary' in position or len(position['summary']) == 0:
      position['summary'] = ' '
    else:
      position['summary'] = position['summary'].replace('\n',r'\\')
      position['summary'] = position['summary'].replace('&',r'\&')

  for education in educations:
    education['period'] = transform_dates(education)
    if not 'notes' in position or len(position['notes']) == 0:
      position['notes'] = ' '
    else:
      position['notes'] = position['notes'].replace('\n',r'\\')
      position['notes'] = position['notes'].replace('&',r'\&')

   
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
