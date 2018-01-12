import argparse
import json

parser = argparse.ArgumentParser(description='Process optional parameters.')
parser.add_argument(
  '--config',
  dest = 'config_path',
  nargs = '?',
  help = 'optional path to the configuration file',
  default = '/home/benrooke/studio_config.json') 

args = parser.parse_args()

access_key_key = 'AccessKey'
username_key = 'Username'
client_number_key = 'ClientNumber'
password_key = 'Password'
org_id_key = 'OrganizationID'
database_key = 'Database'
workdir_key = 'WorkDir'

class Config(object):

  def __init__(self, data):
    self.access_key = data[access_key_key]
    self.username = data[username_key]
    self.client_number = data[client_number_key]
    self.password = data[password_key]
    self.orgID = data[org_id_key]
    self.database = data[database_key]
    self.workdir = data[workdir_key]

  @staticmethod
  def load():
    config_file = open(args.config_path)
    data = json.load(config_file)
    return Config(data)
