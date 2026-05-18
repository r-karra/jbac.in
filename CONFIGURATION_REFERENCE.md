# JBAC - Configuration & Setup Reference

## settings.py Key Configuration

```python
# Basic Settings
SECRET_KEY = os.getenv("SECRET_KEY", "jbac-development-secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")]

# Installed Apps (in order)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'core',
    'accounts',
    'directory',
    'updates',
    'api',
    'meetings',
    'songs',
]

# Custom Authentication Backend (role-based)
AUTHENTICATION_BACKENDS = [
    'config.auth_backends.RoleBasedBackend',
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Database
# SQLite for development, PostgreSQL via Neon for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Or via dj-database-url:
if dj_database_url:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        DATABASES['default'] = dj_database_url.config(
            default=db_url,
            conn_max_age=db_conn_max_age,
            conn_health_checks=True,
            ssl_require=db_ssl_require,
        )
        if 'OPTIONS' not in DATABASES['default']:
            DATABASES['default']['OPTIONS'] = {}
        DATABASES['default']['OPTIONS']['sslmode'] = db_sslmode

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Context Processors
TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'core.context_processors.navigation_groups'
)

# OTP Configuration
OTP_REQUEST_WINDOW_MINUTES = 10  # Max 3 requests per 10 minutes
OTP_MAX_REQUESTS_PER_WINDOW = 3
OTP_MAX_VERIFY_ATTEMPTS = 5
OTP_LOCK_MINUTES = 30
OTP_PROVIDER = os.getenv("OTP_PROVIDER", "console")  # console, twilio, msg91
OTP_TWILIO_ACCOUNT_SID = os.getenv("OTP_TWILIO_ACCOUNT_SID", "")
OTP_TWILIO_AUTH_TOKEN = os.getenv("OTP_TWILIO_AUTH_TOKEN", "")
OTP_TWILIO_FROM_NUMBER = os.getenv("OTP_TWILIO_FROM_NUMBER", "")
OTP_MSG91_AUTH_KEY = os.getenv("OTP_MSG91_AUTH_KEY", "")
OTP_MSG91_SENDER_ID = os.getenv("OTP_MSG91_SENDER_ID", "JBAC")
OTP_MSG91_TEMPLATE_ID = os.getenv("OTP_MSG91_TEMPLATE_ID", "")

# News Configuration
AUTO_PUBLISH_USER_NEWS = os.getenv("AUTO_PUBLISH_USER_NEWS", "True").lower() == "true"

# Songs/Books Configuration
CHRISTIAN_BOOKS_API_URL = os.getenv("CHRISTIAN_BOOKS_API_URL", "")
CHRISTIAN_BOOKS_MAX_RESULTS = os.getenv("CHRISTIAN_BOOKS_MAX_RESULTS", "36")
ANDHRA_CHRISTIAN_SONGS_TIMEOUT_SECONDS = os.getenv("ANDHRA_CHRISTIAN_SONGS_TIMEOUT_SECONDS", "10")

# Admin Site Customization
admin.site.site_header = "JBAC Administration"
admin.site.site_title = "JBAC Admin"
admin.site.index_title = "Community management"
```

---

## .env.example

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,jbac.in
CSRF_TRUSTED_ORIGINS=https://jbac.in,https://www.jbac.in

# Database
# For SQLite (default): omit or leave empty
# For PostgreSQL via Neon:
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
DB_CONN_MAX_AGE=600
DB_SSL_REQUIRE=True
DB_SSLMODE=require

# OTP Configuration
OTP_PROVIDER=console
# For Twilio:
# OTP_PROVIDER=twilio
# OTP_TWILIO_ACCOUNT_SID=your_account_sid
# OTP_TWILIO_AUTH_TOKEN=your_auth_token
# OTP_TWILIO_FROM_NUMBER=+1234567890

# For MSG91:
# OTP_PROVIDER=msg91
# OTP_MSG91_AUTH_KEY=your_auth_key
# OTP_MSG91_SENDER_ID=JBAC
# OTP_MSG91_TEMPLATE_ID=your_template_id

# Features
AUTO_PUBLISH_USER_NEWS=True

# Optional: Custom APIs
CHRISTIAN_BOOKS_API_URL=
CHRISTIAN_BOOKS_MAX_RESULTS=36
ANDHRA_CHRISTIAN_SONGS_TIMEOUT_SECONDS=10
```

---

## requirements.txt

```
dj-database-url==3.1.2
Django==5.1.15
gunicorn==25.1.0
psycopg==3.2.13
Pillow==11.3.0
reportlab==4.2.5
whitenoise==6.12.0
```

**Installation**:
```bash
pip install -r requirements.txt
```

---

## Management Commands

### Data Loading

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load fixtures (if available)
python manage.py loaddata about_page_content navigation_groups

# Dump data (backup)
python manage.py dumpdata --natural-foreign --natural-primary \
  -e contenttypes -e auth.permission > backup.json

# Load data (restore)
python manage.py loaddata backup.json
```

### Collection & Optimization

```bash
# Collect static files
python manage.py collectstatic --noinput

# Compress static files
python manage.py compress

# Clear cache
python manage.py clear_cache
```

---

## Authentication Backend (config/auth_backends.py)

The custom backend handles role-based authentication:

```python
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class RoleBasedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, role=None, **kwargs):
        """
        Authenticate by:
        - identifier: mobile_number OR email
        - password: plain password (Django handles hashing)
        - role: required role match
        """
        try:
            user = User.objects.get(
                Q(mobile_number=username) | Q(email__iexact=username),
                role=role
            )
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
```

---

## Context Processors (core/context_processors.py)

```python
from .models import NavigationGroup

def navigation_groups(request):
    """Provide navigation groups to all templates"""
    groups = NavigationGroup.objects.filter(is_active=True).prefetch_related('items')
    return {'navigation_groups': groups}
```

---

## Common Database Queries

### Get user profile (any role)

```python
from directory.models import get_profile_for_user

profile = get_profile_for_user(request.user)
# Returns BelieverProfile, PastorProfile, etc. based on role
```

### Search approved churches

```python
from directory.models import ChurchProfile

churches = ChurchProfile.objects.filter(
    is_approved=True, 
    is_public=True,
    district='Visakhapatnam'
).select_related('user')
```

### Get featured news

```python
from updates.models import NewsArticle

articles = NewsArticle.objects.filter(
    is_published=True,
    is_featured=True
)[:3]
```

### Get upcoming meetings

```python
from meetings.models import Meeting
from django.utils import timezone

meetings = Meeting.objects.filter(
    is_published=True,
    end_date__gte=timezone.localdate()
).order_by('start_date')
```

---

## Admin Workflows

### Approving User Profiles

1. **Admin Login** → `/admin/`
2. **Directory Section** → Select profile type (PastorProfile, ChurchProfile, etc.)
3. **Select pending profile** (is_approved=False)
4. **Check checkbox**: `is_approved`
5. **Check checkbox**: `is_public` (makes searchable)
6. **Save**

### Publishing News

1. **Admin Login** → `/admin/`
2. **Updates Section** → NewsArticle
3. **Add/Edit article**
4. **Check**: `is_published`
5. **Check**: `is_featured` (shows on homepage)
6. **Set**: `published_at` date/time
7. **Save**

### Managing Navigation

1. **Core Section** → NavigationGroup
2. **Add/Edit group** with title, slug
3. **Add inline NavigationItems**:
   - Set `url_name` (Django reverse name)
   - Set `requires_auth` (hide from unauthenticated)
   - Set `staff_only` (hide from regular users)
4. **Save**

---

## Deployment Checklist

### Pre-Deployment

- [ ] Set `DEBUG=False`
- [ ] Configure `SECRET_KEY` (strong, random)
- [ ] Set `ALLOWED_HOSTS` (production domains)
- [ ] Configure `CSRF_TRUSTED_ORIGINS` (HTTPS origins)
- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure OTP provider (Twilio, MSG91)
- [ ] Set `AUTO_PUBLISH_USER_NEWS` appropriately

### Database Migration

```bash
python manage.py migrate
python manage.py check --deploy
```

### Static Files

```bash
python manage.py collectstatic --noinput
```

### Server

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Environment

```bash
export SECRET_KEY="..."
export DEBUG=False
export ALLOWED_HOSTS="jbac.in,www.jbac.in"
export DATABASE_URL="postgresql://user:pass@host/db"
```

---

## Troubleshooting

### OTP Not Sending

1. Check `OTP_PROVIDER` env variable
2. Verify credentials (Twilio/MSG91)
3. Check `OTP_TWILIO_FROM_NUMBER` format
4. Look at console logs for errors
5. Default: `OTP_PROVIDER=console` (prints to terminal)

### Migration Conflicts

```bash
# Reset migrations (dev only!)
rm */migrations/000*.py
python manage.py makemigrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# Check whitenoise is middleware priority 2
python manage.py check
```

### Database Connection Issues

```bash
# Test connection
python manage.py dbshell

# Check Neon (PostgreSQL)
psql <connection_string>
```

### User Profile Not Found

```python
# Ensure profile exists
from directory.models import BelieverProfile
profile, created = BelieverProfile.objects.get_or_create(
    user=request.user
)
```

---

## Testing

### Run All Tests

```bash
python manage.py test

# Verbose output
python manage.py test --verbosity=2

# Specific app
python manage.py test accounts

# Specific test
python manage.py test accounts.tests.LoginTestCase.test_login
```

### Create Test Data

```bash
# Create fixtures
python manage.py dumpdata > fixtures.json

# Load in tests
python manage.py test --fixtures fixtures.json
```

---

## Performance Optimization

### Database Queries

```python
# Use select_related for ForeignKeys
profiles = PastorProfile.objects.select_related('user').all()

# Use prefetch_related for reverse relations
groups = NavigationGroup.objects.prefetch_related('items').all()

# Use only() to limit fields
users = User.objects.only('id', 'mobile_number').all()
```

### Caching

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def news_list(request):
    # ...
```

### Database Indexes

```python
class Meeting(models.Model):
    # ...
    class Meta:
        indexes = [
            models.Index(fields=['is_published', '-start_date']),
            models.Index(fields=['district', 'state']),
        ]
```

---

## Security Best Practices

1. **Never commit .env file** - Add to .gitignore
2. **Use strong SECRET_KEY** - Generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
3. **Enable HTTPS** - Set `CSRF_TRUSTED_ORIGINS` correctly
4. **Rate limiting** - Already implemented for OTP (3 per 10 min, 30 min lockout)
5. **CSRF protection** - Already enabled via middleware
6. **SQL injection** - Django ORM prevents (use parameterized queries)
7. **XSS protection** - Template auto-escaping enabled
8. **Password hashing** - Django's PBKDF2 by default
9. **CORS** - Not currently enabled (check if needed for APIs)

---

## API Documentation

### GET /api/stats/
Returns platform statistics

**Response**:
```json
{
  "status": "ok",
  "data": {
    "believers": 45,
    "pastors": 23,
    "students": 12,
    "churches": 18,
    "organizations": 5
  }
}
```

### GET /api/pastors/
Search approved pastors

**Parameters**:
- `q` (optional): Search query
- `district` (optional): Filter by district
- `state` (optional): Filter by state

**Response**:
```json
{
  "status": "ok",
  "count": 2,
  "data": [
    {
      "pastor_name": "John Doe",
      "church_name": "Grace Church",
      "district": "Visakhapatnam",
      "state": "Andhra Pradesh",
      "mobile": "+91-XXXXXXXXXX",
      "email": "john@example.com"
    }
  ]
}
```

### GET /api/churches/
Search approved churches with coordinates

**Parameters**: Same as `/api/pastors/` plus latitude/longitude in response

### GET /api/news/
Get published news articles (max 30)

**Response**:
```json
{
  "status": "ok",
  "count": 5,
  "data": [
    {
      "title": "Article Title",
      "slug": "article-title",
      "summary": "Summary text",
      "published_at": "2026-05-18T10:00:00Z"
    }
  ]
}
```

---

## File Structure Summary

```
jbac.in/
├── config/                          # Main Django config
│   ├── settings.py                 # Settings
│   ├── urls.py                     # Root URL config
│   ├── wsgi.py                     # WSGI entry point
│   ├── asgi.py                     # ASGI entry point
│   └── auth_backends.py            # Custom authentication
├── accounts/                        # User authentication
│   ├── models.py                   # User, OTPChallenge
│   ├── views.py                    # Login, OTP
│   ├── forms.py                    # Auth forms
│   ├── urls.py                     # Auth URLs
│   ├── admin.py                    # Admin config
│   └── otp_services.py             # OTP delivery
├── directory/                       # Profiles & search
│   ├── models.py                   # Profile models
│   ├── views.py                    # Registration, search, map
│   ├── forms.py                    # Registration forms
│   ├── urls.py                     # Directory URLs
│   └── admin.py                    # Admin config
├── updates/                         # News & announcements
│   ├── models.py                   # NewsArticle
│   ├── views.py                    # News CRUD
│   ├── forms.py                    # News forms
│   ├── urls.py                     # News URLs
│   └── admin.py                    # Admin config
├── meetings/                        # Event scheduling
│   ├── models.py                   # Meeting model
│   ├── views.py                    # Meeting CRUD
│   ├── forms.py                    # Meeting forms
│   ├── urls.py                     # Meeting URLs
│   └── admin.py                    # Admin config
├── core/                            # Site core
│   ├── models.py                   # About, Navigation models
│   ├── views.py                    # Core views
│   ├── urls.py                     # Core URLs
│   ├── admin.py                    # Admin config
│   └── context_processors.py       # Template context
├── api/                             # JSON APIs
│   ├── views.py                    # API endpoints
│   └── urls.py                     # API URLs
├── songs/                           # Songs/hymns library
│   ├── views.py                    # Song/book search
│   └── urls.py                     # Song URLs
├── templates/                       # HTML templates
│   ├── base.html                   # Base template
│   ├── core/                        # Core templates
│   ├── accounts/                    # Auth templates
│   ├── directory/                   # Directory templates
│   ├── updates/                     # News templates
│   ├── meetings/                    # Meeting templates
│   └── songs/                       # Song templates
├── static/                          # Static files (dev)
│   ├── css/site.css
│   └── js/site.js
├── media/                           # User uploads
│   ├── core/about/
│   ├── meetings/posters/
│   └── updates/news/
├── migrations/                      # DB migrations
├── manage.py                        # Django CLI
├── requirements.txt                 # Python dependencies
├── runtime.txt                      # Python version (for PythonAnywhere)
├── .env                             # Environment variables (gitignored)
├── .gitignore
├── README.md
└── db.sqlite3                       # SQLite database (dev)
```

---

## Quick Start Commands

```bash
# Clone repo
git clone https://github.com/r-karra/jbac_core.git
cd jbac_core

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver

# Access at http://127.0.0.1:8000
# Admin at http://127.0.0.1:8000/admin
```

---

**Last Updated**: 2026-05-18
**Framework**: Django 5.1.15
**Python**: 3.12+
**License**: Refer to repository

