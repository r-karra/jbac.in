# JBAC

JBAC is a Django application for Jesus Believers Association Council. It provides role-based registrations, searchable pastor and church directory listings, a news section, contact details, and an admin workflow for approving records before they become public.

## Features

- Multi-role authentication using mobile number or email plus password
- OTP login flow for role-based access
- Separate registration flows for believers, pastors, students, churches, and organizations
- Public pastor and church search with district and state filters
- District map search for church locations with Leaflet and OpenStreetMap
- Meeting submission form with admin verification and upcoming meetings filters
- News publishing and content management through Django admin
- Downloadable PDF member ID card for logged-in users
- Admin operations dashboard for pending approval monitoring
- JSON API endpoints for stats, pastors, churches, and news
- Bilingual English and Telugu interface copy with a mobile-first responsive layout
- Deployment-ready settings for SQLite in development and PostgreSQL in production

## Local Setup

1. Create and activate a Python 3.12 virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run migrations with `python manage.py migrate`.
4. Create an admin account with `python manage.py createsuperuser`.
5. Start the server with `python manage.py runserver`.

## Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: `True` or `False`
- `ALLOWED_HOSTS`: comma-separated hosts, for example `jbac.in,www.jbac.in`
- `CSRF_TRUSTED_ORIGINS`: comma-separated origins for production HTTPS deployments
- `DATABASE_URL`: optional database URL. If omitted, SQLite is used.
- `DB_CONN_MAX_AGE`: database persistent connection lifetime in seconds (default `600`)
- `DB_SSL_REQUIRE`: force SSL when parsing Postgres URLs with `dj-database-url` (default `True`)
- `DB_SSLMODE`: Postgres SSL mode added to connection options when using Postgres (default `require`)
- `AUTO_PUBLISH_USER_NEWS`: `True` to publish logged-in user submissions immediately, `False` to require admin approval
- `OTP_PROVIDER`: `console`, `twilio`, or `msg91`
- `OTP_TWILIO_ACCOUNT_SID`: Twilio account SID (required when `OTP_PROVIDER=twilio`)
- `OTP_TWILIO_AUTH_TOKEN`: Twilio auth token (required when `OTP_PROVIDER=twilio`)
- `OTP_TWILIO_FROM_NUMBER`: Twilio sender number (required when `OTP_PROVIDER=twilio`)
- `OTP_MSG91_AUTH_KEY`: MSG91 auth key (required when `OTP_PROVIDER=msg91`)
- `OTP_MSG91_SENDER_ID`: MSG91 sender ID (optional)
- `OTP_MSG91_TEMPLATE_ID`: MSG91 OTP template ID (optional but recommended)

Example:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:password@hostname:5432/jbac
OTP_PROVIDER=console
```

## Neon PostgreSQL Setup

Use one Neon Postgres database for the entire Django website (all apps share Django's single `default` database).

1. Create a Neon project and database from the Neon dashboard.
2. Copy the connection string from Neon (`Connection Details`).
3. Set environment variables:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>/<dbname>?sslmode=require
DB_SSL_REQUIRE=True
DB_SSLMODE=require
```

4. Apply schema to Neon:

```bash
python manage.py migrate
```

5. (Optional) Move existing SQLite data into Neon:

```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission > data.json
python manage.py loaddata data.json
```

6. Verify DB connection:

```bash
python manage.py showmigrations
python manage.py check
```

## Tests

Run all tests with:

`python manage.py test`

## About Page Seeding

Seed or refresh About Us submenu admin pages:

`python manage.py seed_about_pages`

Reset all current About page content and reseed defaults:

`python manage.py seed_about_pages --reset`

## Admin Workflow

Use Django admin to:

- Review registrations
- Mark profiles as approved
- Mark pastor and church records as public for directory search
- Publish and feature news articles

## Deployment

This repository includes a `Dockerfile` for container-based deployment.

### PythonAnywhere

Use a WSGI file that points Python to the project root before Django loads settings.

Example `/var/www/<username>_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

project_home = "/home/<username>/jbac.in"
if project_home not in sys.path:
	sys.path.insert(0, project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
```

Also make sure the PythonAnywhere web app is using the same virtualenv where you installed the project requirements:

```bash
mkvirtualenv --python=/usr/bin/python3.10 jbac-env
workon jbac-env
pip install -r /home/<username>/jbac.in/requirements.txt
```

Then in the Web tab:

- Set the source code path to `/home/<username>/jbac.in`
- Set the virtualenv path to `/home/<username>/.virtualenvs/jbac-env`
- Reload the web app after saving the WSGI file

If `DATABASE_URL` is not set, the project falls back to SQLite.

### AWS

- Build the image and push it to ECR.
- Run it on ECS, App Runner, or Elastic Beanstalk with the environment variables above.
- Attach an RDS PostgreSQL instance and set `DATABASE_URL`.

### GCP

- Build and deploy the container to Cloud Run.
- Attach a Cloud SQL PostgreSQL instance and set `DATABASE_URL`.
- Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` for the production domain.

## Default Routes

- `/` home page
- `/accounts/login/` login
- `/accounts/otp/` OTP login request
- `/directory/register/` registration hub
- `/directory/search/` church and pastor search
- `/directory/map-search/` district map search
- `/directory/member-id/` member ID PDF download (authenticated)
- `/news/` news listing
- `/meetings/submit/` submit meeting details
- `/meetings/view/` view upcoming published meetings
- `/admin-dashboard/` admin operations dashboard (staff only)
- `/api/stats/`, `/api/pastors/`, `/api/churches/`, `/api/news/` JSON APIs
- `/admin/` Django admin