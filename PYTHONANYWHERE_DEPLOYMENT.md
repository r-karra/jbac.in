# PythonAnywhere Deployment Guide

This guide will help you fix the 500 error on PythonAnywhere.

## Common 500 Error Causes and Fixes

### 1. **WSGI File Configuration** (Most Common Issue)

The PythonAnywhere WSGI file needs proper sys.path configuration:

**Steps:**
1. Go to https://www.pythonanywhere.com/web_app_setup/
2. Click on your web app (rkarra.pythonanywhere.com)
3. Under "Code", find the WSGI configuration file path (usually `/var/www/rkarra_pythonanywhere_com_wsgi.py`)
4. Copy the entire contents from `pythonanywhere_wsgi.py` file in the repository
5. Replace the content with proper paths:
   - Change `rkarra` to your actual PythonAnywhere username (if different)
   - Ensure virtualenv path is correct (check your virtualenv location)
6. Save the file

### 2. **Collect Static Files**

After every deployment:
```bash
python manage.py collectstatic --no-input
```

### 3. **Install/Update Dependencies**

Make sure your virtualenv has all requirements:
```bash
# Activate your virtualenv (or use PythonAnywhere's built-in one)
pip install -r requirements.txt
```

### 4. **Environment Variables**

1. Follow these steps in PythonAnywhere console:
   ```bash
   # Navigate to your project
   cd /home/rkarra/jbac.in
   
   # Create .env file with proper values
   nano .env
   ```

2. Use `.env.example` as template, but fill in:
   - `SECRET_KEY`: Generate a strong random key or run:
     ```bash
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - `DATABASE_URL`: Your Neon PostgreSQL connection string (from Neon dashboard)
   - `DEBUG=False` for production
   - Other OTP/API keys as needed

3. Make sure `.env` is NOT tracked in git:
   ```bash
   # Already in .gitignore, but verify:
   cat .gitignore | grep ".env"
   ```

### 5. **Database Migration**

If static files or database schema changed:
```bash
python manage.py migrate
```

### 6. **Reload Web App**

In PythonAnywhere dashboard:
1. Go to Web app page
2. Click the green "Reload" button
3. Wait a few seconds for changes to take effect

### 7. **Check Error Logs**

If you still get 500 errors:
1. Go to PythonAnywhere dashboard → Web app → "Log files"
2. Check "Error log" for detailed error messages
3. Look for:
   - `ModuleNotFoundError: config` - WSGI file path issue
   - `psycopg` import errors - Missing database driver
   - Database connection errors - Check DATABASE_URL and network access

### 8. **Debug Mode (Temporary)**

To see detailed error messages (NOT recommended for long-term production):
1. Set `DEBUG=True` in `.env`
2. Reload web app
3. Check what the actual error is
4. Set `DEBUG=False` again after fixing

## Quick Troubleshooting Checklist

- [ ] WSGI file has correct sys.path entries with your username
- [ ] WSGI file has correct virtualenv path
- [ ] `.env` file exists with proper SECRET_KEY and DATABASE_URL
- [ ] All requirements installed: `pip install -r requirements.txt`
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] Database migrated: `python manage.py migrate`
- [ ] Web app reloaded in PythonAnywhere dashboard
- [ ] Error log checked for specific error messages

## File Checklist

Make sure these files are in your repository:
- `pythonanywhere_wsgi.py` - Template for PythonAnywhere WSGI
- `.env.example` - Environment variable template
- `.env` - Should exist locally with actual values (NOT in git)
- `config/wsgi.py` - Default Django WSGI
- `config/settings.py` - Django settings
- `requirements.txt` - All dependencies

## Key Settings

In `config/settings.py`:
- `SECRET_KEY` - Loaded from `.env`
- `DEBUG` - Should be `False` in production
- `ALLOWED_HOSTS` - Includes `rkarra.pythonanywhere.com`
- `DATABASES` - Uses `DATABASE_URL` from `.env`
- `STATIC_ROOT` - Set to staticfiles/ directory
