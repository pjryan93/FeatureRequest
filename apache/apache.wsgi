#!/usr/bin/python
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/featurerequest/")
config_name = os.getenv('APP_SETTINGS') 
from app import create_app
application = create_app(config_name)