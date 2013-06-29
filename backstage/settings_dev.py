"""
    Author: weixin
    Email: weixindlut@gmail.com
    Description: Django setting for daily development
    Created: 
"""
from backstage.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PRODUCTION_FLAG = "Development Version!"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'backstagedb',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'gsoc',
        'HOST': 'localhost',
        #'HOST':'192.168.9.172',
        'PORT': '',                      # Set to empty string for default.
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'backstagedb_dev',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'root',
        #'HOST': 'localhost',
        'HOST':'192.168.2.90',
        'PORT': '',                      # Set to empty string for default.
    }
}
"""
