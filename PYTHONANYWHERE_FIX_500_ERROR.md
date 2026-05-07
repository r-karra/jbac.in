# URGENT: How to Fix the 500 Error on PythonAnywhere

## Step 1: Check the Error Log (FIRST DO THIS)

1. Go to https://www.pythonanywhere.com/user/rkarra/webapps/
2. Click on your web app `rkarra.pythonanywhere.com`
3. Scroll down to **"Log files"** section
4. Click on **"Error log"** link
5. **Copy the last 20-30 lines and share them** - this will tell us exactly what's wrong

## Step 2: Verify WSGI Configuration (MOST LIKELY ISSUE)

Your PythonAnywhere WSGI file is probably missing the sys.path configuration.

### Do This Now:

1. In PythonAnywhere dashboard, click on your web app
2. Under "Code" section, find the WSGI configuration file
3. It should say something like: `/var/www/rkarra_pythonanywhere_com_wsgi.py`
4. Click on that file path to edit it
5. Replace **ALL** the content with this:

```python
# This WSGI file handles the Django app on PythonAnywhere
import os
import sys

# IMPORTANT: Add your project directory to Python path
# Replace 'rkarra' with your actual PythonAnywhere username
project_home = '/home/rkarra/jbac.in'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add the virtualenv site-packages to the path
# Find your virtualenv path: go to PythonAnywhere Web App page, look under "Virtual environment"
# It's usually: /home/rkarra/.virtualenvs/<venv_name>
venv_path = '/home/rkarra/.virtualenvs/jbac'  # CHANGE THIS to your actual virtualenv path
if venv_path:
    venv_site_packages = os.path.join(venv_path, 'lib/python3.12/site-packages')
    if venv_site_packages not in sys.path:
        sys.path.insert(0, venv_site_packages)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Set the .env file location (optional but recommended)
os.environ.setdefault('ENV_FILE', '/home/rkarra/jbac.in/.env')

# Load the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Save the file
7. Go back to Web app dashboard and click the green **"Reload"** button

## Step 3: Setup Bash Console Commands

If WSGI still doesn't work, run these in PythonAnywhere Bash console:

```bash
# Navigate to your project
cd /home/rkarra/jbac.in

# Activate your virtualenv
source /home/rkarra/.virtualenvs/jbac/bin/activate  # ADJUST path to your virtualenv

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Verify settings load
python manage.py check
```

## Step 4: Find Your Correct Virtualenv Path

1. In PythonAnywhere, click on **"Web"** tab
2. Click on your web app name
3. Look for **"Virtual environment"** section
4. You'll see something like: `/home/rkarra/.virtualenvs/jbac-env`
5. **Use THIS path** in the WSGI file above (not the generic one I provided)

## Step 5: After Making Changes

1. Update the WSGI file with your correct paths
2. Click **"Reload"** button in Web app page
3. Wait 10 seconds
4. Visit https://rkarra.pythonanywhere.com/
5. Check if it works

## Common 500 Errors & Solutions

### Error 1: ModuleNotFoundError: config
**Cause:** WSGI sys.path is not configured correctly
**Fix:** Update sys.path in WSGI file with correct project path

### Error 2: ModuleNotFoundError: psycopg
**Cause:** Database driver not installed
**Fix:** Run `pip install psycopg==3.2.13` in virtualenv

### Error 3: Database connection error
**Cause:** DATABASE_URL not set or invalid
**Fix:** 
- Verify `.env` has correct DATABASE_URL
- Test connection in bash console: `python manage.py dbshell`

### Error 4: TemplateDoesNotExist
**Cause:** Static files not collected
**Fix:** Run `python manage.py collectstatic --no-input`

### Error 5: ALLOWED_HOSTS error
**Cause:** Hostname not in ALLOWED_HOSTS
**Fix:** Already fixed in .env, but you may need to reload web app

---

## QUICK CHECKLIST

- [ ] Checked error log in PythonAnywhere (Step 1)
- [ ] Updated WSGI file with correct sys.path (Step 2)
- [ ] Found correct virtualenv path (Step 4)
- [ ] Clicked Reload button in Web app
- [ ] Ran `pip install -r requirements.txt` in bash
- [ ] Ran `python manage.py migrate` in bash
- [ ] Ran `python manage.py collectstatic --no-input` in bash
- [ ] Ran `python manage.py check` to verify no errors

---

## Need Help?

1. First, **share the error log** (Step 1)
2. Run `python manage.py check` and share any errors
3. Tell me what paths you found in Step 4

This will help me debug exactly what's wrong!
