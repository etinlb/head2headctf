# config.py
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

# Enable Flask's debugging features. Should be False in production
DEBUG = True
PREFERRED_URL_SCHEME = 'https'
DATABASE_FILE = "data.db"
SQLALCHEMY_DATABASE_URI = "sqlite:////{}/{}".format(dir_path, DATABASE_FILE)

# Custom configuration data. Some could probably be in a database
TIMER_AMOUNT = 600
