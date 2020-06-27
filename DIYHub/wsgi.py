import os

import sys

sys.path.append('/opt/bitnami/apps/django/django_projects/DIYHub')

os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/DIYHub/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DIYHub.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
