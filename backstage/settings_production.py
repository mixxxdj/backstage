"""
    Author: weixin
    Email: weixindlut@gmail.com
    Description: Django setting for daily development
    Created: 2013-06-20
"""

from backstage.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PRODUCTION_FLAG = "Technical Preview!" 

#TODO: we should deploy production environment in the further
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'backstagedb_pro',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}
