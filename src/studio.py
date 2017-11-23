import argparse
from cookielib import CookieJar
import json
import urllib
import urllib2

parser = argparse.ArgumentParser(description='Process optional parameters.')
parser.add_argument(
  '--config',
  dest = 'config_path',
  nargs = '?',
  help = 'optional path to the configuration file',
  default = '/opt/studio/config.json')

args = parser.parse_args()

config_data = None

access_key_key = 'AccessKey'
username_key = 'Username'
client_number_key = 'ClientNumber'
password_key = 'Password'
org_id_key = 'OrganizationID'

class Config(object):

  def __init__(self, data):
    self.access_key = data[access_key_key]
    self.username = data[username_key]
    self.client_number = data[client_number_key]
    self.password = data[password_key]
    self.orgID = data[org_id_key]

  @staticmethod
  def open():
    config_file = open(args.config_path)
    data = json.load(config_file)
    return Config(data)


class Member:
  def __init__(self, full_name, scanID):
    self.full_name = full_name
    self.attendance = 0

config = Config.open()

member_guids = {}

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
  login()
  resp = opener.open(URL + URI_records + '?tableName=attendance')
  return json.load(resp)

def contacts():
  login()
  resp = opener.open(URL + URI_records + '?tableName=Contact')
  return json.load(resp)

def main():
  all_contacts = contacts()
  for c in all_contacts:
    guid = c["ID"]
    full_name = c["FullNameSimple"].encode('utf-8').strip()
    scanID = c.get("PerfectScanID", "")
    member = Member(full_name, scanID)
    member_guids[guid] = member

  all_attendance = attendance()
  for anAttendance in all_attendance:
    if anAttendance["Status"] == "Attended":
      member = member_guids.get(anAttendance["Attendee"])
      if member is not None:
        member.attendance += 1

  for _, v in member_guids.iteritems():
    print("{} : {}".format(v.attendance, v.full_name))

def main2():
  print(contacts())

if __name__ == '__main__':
  main2()
