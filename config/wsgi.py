import os

from django.core.wsgi import get_wsgi_application
from wsgi_basic_auth import BasicAuth

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = BasicAuth(get_wsgi_application())
