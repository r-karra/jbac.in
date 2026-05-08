import os
import sys

project_home = '/home/rkarra/jbac.in'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

venv_path = '/home/rkarra/.virtualenvs/jbacenv'
venv_site_packages = os.path.join(venv_path, 'lib/python3.12/site-packages')
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
