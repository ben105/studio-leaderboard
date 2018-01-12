import argparse
from cookielib import CookieJar
from datetime import datetime
import json
import os 
import sys
import urllib
import urllib2
from config import *

config = Config.load()

headers = [
  ('X-Access-Key', config.access_key),
  ('X-Client-Number', config.client_number),
  ('X-Username', config.username),
  ('X-Password', config.password),
]

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = headers

URL = 'https://studiokickslosgatos.perfectmind.com'
URI_login = '/api/2.0/B2C/Login'
URI_records = '/api/2.0/B2C/ObjectRecords'
URI_objects = '/api/2.0/B2C/Objects'
URI_query = '/api/2.0/B2C/Query'

last_updated_path = os.path.join(config.workdir, 'last_updated.out')

def last_updated():
  if not os.path.isfile(last_updated_path):
    return None
  with open(last_updated_path) as datefile:
    return datefile.read().strip()
  return None

def update():
  with open(last_updated_path, 'w') as datefile:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    datefile.write(now)

def login():
  get_query = {
    'orgId': config.orgID,
    'username': config.username,
    'password': config.password
  }
  resp = opener.open(URL + URI_login + '?' + urllib.urlencode(get_query))
  login_data = json.load(resp)
  # Idempotent. We reassign headers because we don't want to re-append the auth token everytime time.
  opener.addheaders = headers
  opener.addheaders.append( ('X-Auth-Token', login_data["UserID"]) )

def attendance(last_updated):
  return query('Attendance', last_updated)

def contacts(last_updated):
  return query('Contact', last_updated)

def events(last_updated):
  return query('Event', last_updated)

def teachers(last_updated):
  return query('Teachers', last_updated)

def transactions(last_updated):
  return query('Transaction', last_updated)

def query_object(name):
  resp = opener.open(URL + URI_records + '?tableName={}'.format(name))
  return json.load(resp)

def objects():
  resp = opener.open(URL + URI_objects)
  return json.load(resp)

def query(table, last_updated):
  query_string = 'SELECT * FROM Custom.{}'.format(table)
  if last_updated:
    query_string += ' WHERE Custom.{}.CreatedDate > convert(datetime, \'{}\')'.format(table, last_updated)
  opener.addheaders.append( ('Content-Type', 'application/json') )
  data = {
    'QueryString': query_string
  }
  resp = opener.open(URL + URI_query, urllib.urlencode(data))
  update()
  return json.load(resp)

def test_query(query_string):
  opener.addheaders.append( ('Content-Type', 'application/json') )
  data = {
    'QueryString': query_string
  }
  resp = opener.open(URL + URI_query, urllib.urlencode(data))
  return resp

