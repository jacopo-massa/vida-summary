import os

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dotenv import load_dotenv

DB_DIR = "/img/"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load env variables
# if hosted, need to set up CONFIG VARIABLES !!!

load_dotenv(os.path.join(ROOT_DIR, ".env"))

REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')

dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=REFRESH_TOKEN)
