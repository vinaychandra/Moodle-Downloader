import os
import os.path
from ConfigParser import ConfigParser

conf = ConfigParser()
project_dir = os.path.dirname(os.path.abspath(__file__))
conf.read(os.path.join(project_dir, 'config.ini'))


root_directory = conf.get("dirs", "root_dir")
username = conf.get("auth", "username")
password = conf.get("auth", "password")
authentication_url = conf.get("auth", "url")