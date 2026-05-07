# This is the WSGI file to use on PythonAnywhere
# On PythonAnywhere, this should be placed at: /var/www/rkarra_pythonanywhere_com_wsgi.py
# Or use this content in the web app's WSGI file configuration

import os
import sys
from pathlib import Path

# Add your project directory to the sys.path
# Replace 'rkarra' with your actual username
project_home = '/home/rkarra/jbac.in'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add the virtualenv site-packages to the path
# Replace 'rkarra' with your actual username
venv_path = '/home/rkarra/.virtualenvs/jbac'  # or wherever your virtualenv is
venv_site_packages = os.path.join(venv_path, 'lib/python3.12/site-packages')
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
