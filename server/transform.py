from itertools import izip
import logging

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)


def transform_date(date):
    res = ''
    if 'month' in date:
      res = res + str(date['month']) + '/'
    if 'year' in date:
      res = res + str(date['year']) 
    return res

def transform_dates(position):
    if not 'startDate' in position: 
      startDate = ''
    else:
      startDate = transform_date(position['startDate'])

    if 'isCurrent' in position and (position['isCurrent'] == 'true' or position['isCurrent'] == True):
      endDate = 'present'
    elif 'endDate' in position: 
      endDate = transform_date(position['endDate'])
    else:
      endDate = ''

    return "%s - %s" % (startDate, endDate)

def sanitize_dict(dictionary):
  for k, v in dictionary.iteritems():
    dictionary[k] = sanitize_item(v)

    #if isinstance(v, dict):
    #  dictionary[k] = sanitize_dict(v)
    # elif isinstance(v, list):
    #   dictionary[k] = [sanitize_item(x) for x in v]
    #elif isinstance(v, basestring):
    #  dictionary[k] = sanitize_str(v)
    #else:
    #  dictionary[k] = v

  return dictionary

def sanitize_item(v):
    if isinstance(v, dict):
       v = sanitize_dict(v)
    elif isinstance(v, list):
       v = [sanitize_item(x) for x in v]
    elif isinstance(v, basestring):
       v = sanitize_str(v)
    return v
 
def sanitize_str(s):
  result = s
  result = result.replace('\n',r'\\')
  # &lsquo;
  result = result.replace(unichr(0x2018),"`")
  result = result.replace(unichr(0x2019),"'")
  result = result.replace(unichr(0x201C),"``")
  result = result.replace(unichr(0x201D),"''")
  result = result.replace(unichr(0x2014),"---")
  for special_char in ['&','%','$','_','^','#','~','{','}']:
    result = result.replace(special_char,'\\' + special_char)
  return result

def replace_missing_keys(dictionary, keys):
   for k in keys:
    if not k in dictionary:
      dictionary[k] = ''

def transform_linkedin(profile):
  #logging.debug("transforming %s" % profile)
  #for key, value in profile.iteritems() :
  #  print key, value

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
    replace_missing_keys(position, ['summary'])

  for education in educations:
    education['period'] = transform_dates(education)
    replace_missing_keys(education, ['notes'])
   
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

  context = sanitize_dict(context)

  return context
