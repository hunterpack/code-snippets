from configparser import ConfigParser
from os import environ

config = ConfigParser()
config.read("config/config.ini")
ENVIRONMENT = environ.get("RUNENV", "LOCAL").upper()
props = config[ENVIRONMENT]

LOG_FOLDER = props["log_folder"]