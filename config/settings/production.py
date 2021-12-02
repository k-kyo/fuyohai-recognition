import os

import django_heroku
import dj_database_url

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)

DATABASES = {
    'default': db_from_env
}

django_heroku.settings(locals())
