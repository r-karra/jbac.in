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