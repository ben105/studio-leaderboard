import argparse
from cookielib import CookieJar
import json
import os 
import sys
import urllib
import urllib2
from config import *

class Member:
  def __init__(self, full_name, scanID):
    self.full_name = full_name
    self.attendance = 0

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

def attendance():
  return query_object('Attendance')

def contacts():
  return query_object('Contact')

def events():
  return query_object('Event')

def teachers():
  return query_object('Teachers')

def transactions():
  return query_object('Transaction')

def query_object(name):
  login()
  resp = opener.open(URL + URI_records + '?tableName={}'.format(name))
  return json.load(resp)

def objects():
  login()
  resp = opener.open(URL + URI_objects)
  return json.load(resp)

