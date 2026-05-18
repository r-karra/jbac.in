# JBAC Project Summary & Architecture

## Executive Summary

**JBAC** (Jesus Believers Association Council) is a Django-based community platform for Christians in Andhra Pradesh and Telangana. It enables secure, role-based registrations for 8 user types, provides a searchable pastor/church directory, publishes news, manages events, and offers a songs/hymns library.

**Repository**: https://github.com/r-karra/jbac_core  
**Live Site**: rkarra.pythonanywhere.com  
**Framework**: Django 5.1.15 + Python 3.12+  
**Database**: SQLite (dev) / PostgreSQL/Neon (production)  
**Bilingual**: English + Telugu

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Templates)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  base.html (Navigation, Footer, Language Switcher)  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌─────────────────┬──────────────┬──────────────────────┐  │
│  │  core/          │ accounts/    │ directory/           │  │
│  │  - home.html    │ - login      │ - register_landing   │  │
│  │  - about.html   │ - otp        │ - registration_form  │  │
│  │  - contact      │ - logout     │ - search.html        │  │
│  └─────────────────┴──────────────┴──────────────────────┘  │
│  ┌─────────────────┬──────────────┬──────────────────────┐  │
│  │ updates/        │ meetings/    │ songs/               │  │
│  │ - news_list     │ - submit     │ - search.html        │  │
│  │ - news_detail   │ - view       │ - books.html         │  │
│  │ - submit        │ - detail     │                      │  │
│  └─────────────────┴──────────────┴──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   ROUTING LAYER (URLs)                      │
│  config/urls.py routes to app-level urls.py files          │
│  Pattern: /app-name/path/ → app.views.view_name           │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   LOGIC LAYER (Views)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FBVs & CBVs handling requests, forms, redirects     │   │
│  │  - LoginView, OTPRequestView, OTPVerifyView          │   │
│  │  - search_directory, map_search, member_id_pdf       │   │
│  │  - news_list, news_detail, submit_news              │   │
│  │  - submit_meeting, view_meetings, meeting_detail     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Views (JSON endpoints)                          │   │
│  │  - platform_stats_api, pastors_api, churches_api     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   FORMS LAYER                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  StyledFormMixin → Auto CSS classes on widgets      │   │
│  │  LoginForm, OTPRequestForm, OTPVerifyForm            │   │
│  │  BaseRegistrationForm (abstract)                     │   │
│  │    ├─ BelieverRegistrationForm                       │   │
│  │    ├─ PastorRegistrationForm                         │   │
│  │    ├─ StudentRegistrationForm                        │   │
│  │    ├─ ChurchRegistrationForm                         │   │
│  │    └─ OrganizationRegistrationForm                   │   │
│  │  MeetingSubmissionForm, MeetingFilterForm            │   │
│  │  NewsSubmissionForm, NewsAdminForm                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE LAYER (Models)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  User (custom, AbstractUser + mobile + role)         │   │
│  │  OTPChallenge (for OTP auth flow)                    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  DIRECTORY:                                          │   │
│  │  ApprovalFields (abstract base)                      │   │
│  │    ├─ BelieverProfile                               │   │
│  │    ├─ PastorProfile                                 │   │
│  │    ├─ StudentProfile                                │   │
│  │    ├─ ChurchProfile                                 │   │
│  │    └─ OrganizationProfile                           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  NewsArticle (updates app)                           │   │
│  │  Meeting (meetings app)                             │   │
│  │  AboutPageContent (core app)                        │   │
│  │  NavigationGroup + NavigationItem (core app)        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   PERSISTENCE LAYER                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SQLite (Development)  │  PostgreSQL/Neon (Prod)     │   │
│  │  db.sqlite3            │  DATABASE_URL via Neon      │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Media Storage: /media/ (Uploads)                    │   │
│  │    ├─ meetings/posters/                             │   │
│  │    ├─ updates/news/                                 │   │
│  │    └─ core/about/                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Static Files: /static/ (CSS, JS, Images)           │   │
│  │    Served by WhiteNoise (whitenoise middleware)      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Model Relationships

```
┌─────────────────────┐
│      User (auth)    │
├─────────────────────┤
│ id (PK)             │
│ mobile_number (UK)  │◄────────────┐
│ email (UK)          │◄──┐         │
│ role (choices)      │   │         │
│ member_id (UK)      │   │         │
│ first_name          │   │         │
│ last_name           │   │         │
│ is_active           │   │         │
│ is_staff            │   │         │
└─────────────────────┘   │         │
        ▲                 │         │
        │                 │         │
        │ OneToOne        │         │
        │ (per role)      │         │
        ▼                 │         │
┌─────────────────────┐   │         │
│ BelieverProfile     │───┘         │
├─────────────────────┤             │
│ user (PK, FK)       │             │
│ full_name           │             │
│ gender              │             │
│ date_of_birth       │             │
│ is_approved         │             │
│ is_public           │             │
└─────────────────────┘             │
                                    │
┌──────────────────────┐            │
│ PastorProfile        │            │
├──────────────────────┤            │
│ user (PK, FK)────────┼────────────┘
│ pastor_name          │
│ church_name          │
│ district             │
│ latitude/longitude   │
│ is_approved          │
│ is_public            │
└──────────────────────┘

Similar OneToOne relations for:
- StudentProfile
- ChurchProfile
- OrganizationProfile

┌──────────────────────┐
│ OTPChallenge         │
├──────────────────────┤
│ id (PK)              │
│ user (FK)────┐       │
│ code         │ Many  │
│ expires_at   │ OTPs  │
│ is_used      │ per   │
│ failed_attempts      │
└──────────────────────┘

┌──────────────────────┐
│ NewsArticle          │
├──────────────────────┤
│ id (PK)              │
│ title                │
│ slug (UK)            │
│ category             │
│ is_published         │
│ is_featured          │
│ published_at         │
└──────────────────────┘

┌──────────────────────┐
│ Meeting              │
├──────────────────────┤
│ id (PK)              │
│ title                │
│ start_date           │
│ end_date             │
│ district             │
│ latitude/longitude   │
│ is_published         │
└──────────────────────┘

┌──────────────────────┐
│ NavigationGroup      │
├──────────────────────┤
│ id (PK)              │
│ slug (UK)            │ OneToMany
│ title_en             │ to
│ title_te             │ NavigationItem
└──────────────────────┘
        ▲
        │ contains
        ▼
┌──────────────────────┐
│ NavigationItem       │
├──────────────────────┤
│ id (PK)              │
│ group (FK)           │
│ title_en/te          │
│ url_name             │
│ url_path             │
│ requires_auth        │
│ staff_only           │
└──────────────────────┘

┌──────────────────────┐
│ AboutPageContent     │
├──────────────────────┤
│ id (PK)              │
│ section_slug (UK)    │
│ menu_title_en/te     │
│ page_title_en/te     │
│ description          │
│ youtube_embed_url    │
│ image (FileField)    │
│ pdf (FileField)      │
└──────────────────────┘
```

---

## App Breakdown & Responsibilities

| App | Purpose | Key Models | Key Views | Auth Required |
|-----|---------|-----------|-----------|---------------|
| **accounts** | Authentication & user mgmt | User, OTPChallenge | LoginView, OTPRequestView, OTPVerifyView | No (login views) |
| **directory** | Profiles & search | 5 Profile models | registration_landing, register_category, search_directory, map_search | Partial (register public, search public) |
| **updates** | News & announcements | NewsArticle | news_list, news_detail, submit_news | Partial (submit requires auth) |
| **meetings** | Event scheduling | Meeting | submit_meeting, view_meetings, meeting_detail | Partial (submit requires auth) |
| **core** | Site core & navigation | AboutPageContent, NavigationGroup, NavigationItem | home, about, navigation_group_page | Partial (some sections auth-only) |
| **api** | JSON endpoints | (none, query-based) | platform_stats_api, pastors_api, churches_api, news_api | No (public) |
| **songs** | Library & resources | (none, external APIs) | songs_search, books_list | No (public) |

---

## User Authentication Flow

```
┌─────────────────────────────────────────────────────────┐
│              User Visits Login Page                     │
└─────────────────────────────────────────────────────────┘
                        ▼
                  ┌──────────────┐
                  │ Two Options: │
                  │ 1. Password  │
                  │ 2. OTP       │
                  └──────────────┘
                        ▼
                    ┌─────────────────────────────────┐
            ┌──────►│ Path 1: Password Login          │
            │       ├─────────────────────────────────┤
            │       │ 1. Select Role                  │
            │       │ 2. Enter Mobile/Email           │
            │       │ 3. Enter Password               │
            │       │ 4. LoginForm validation         │
            │       │ 5. Check rate limits            │
            │       │ 6. login() → Session            │
            │       │ 7. Redirect to dashboard        │
            │       └─────────────────────────────────┘
            │
   ┌────────┴────────┐
   │                 ▼
   │        ┌──────────────────────────────┐
   └───────►│ Path 2: OTP Login            │
            ├──────────────────────────────┤
            │ 1. Select Role               │
            │ 2. Enter Mobile/Email        │
            │ 3. Check rate limit (3/10m)  │
            │ 4. Generate OTP (6 digits)   │
            │ 5. Store OTPChallenge        │
            │ 6. Send via OTP_PROVIDER:    │
            │    - console (print)         │
            │    - twilio (SMS)            │
            │    - msg91 (SMS)             │
            │ 7. Redirect to OTP verify    │
            │ 8. User enters OTP code      │
            │ 9. Validate (check expiry,   │
            │    used status, lock)        │
            │ 10. Track failed attempts    │
            │ 11. Lock after 5 failed (30m)│
            │ 12. Success: login()         │
            │ 13. Redirect to dashboard    │
            └──────────────────────────────┘

Database flow:
User → OTPChallenge → code verified → is_used=True → login()
```

---

## Registration Flow by Role

```
┌────────────────────────────────────┐
│  User visits /directory/register/  │
├────────────────────────────────────┤
│  registration_landing() shows 5    │
│  options:                          │
│  1. Believer                       │
│  2. Pastor                         │
│  3. Student                        │
│  4. Church                         │
│  5. Organization                   │
└────────────────────────────────────┘
              ▼
┌────────────────────────────────────┐
│ User selects role → form page      │
├────────────────────────────────────┤
│ register_category(category=role)   │
│ Displays appropriate form:         │
│ - BelieverRegistrationForm         │
│ - PastorRegistrationForm           │
│ - StudentRegistrationForm          │
│ - ChurchRegistrationForm           │
│ - OrganizationRegistrationForm     │
└────────────────────────────────────┘
              ▼
┌────────────────────────────────────┐
│ User fills form:                   │
│ - Common fields: mobile, email,    │
│   password (2x), consent checkbox  │
│ - Role-specific fields:            │
│   names, gender, locations, etc.   │
│                                    │
│ BaseRegistrationForm validation:   │
│ - mobile_number unique check       │
│ - email unique check               │
│ - password match check             │
│ - consent checkbox required        │
└────────────────────────────────────┘
              ▼
┌────────────────────────────────────┐
│ Form.save() (POST success)         │
├────────────────────────────────────┤
│ 1. Create User instance:           │
│    - mobile_number (USERNAME_FIELD)│
│    - role=selected_role            │
│    - Generate member_id            │
│    - Set confidentiality_ack=True  │
│                                    │
│ 2. Create Profile (1:1 with User)  │
│    - BelieverProfile, etc.         │
│    - is_approved=False (default)   │
│    - is_public=False (default)     │
│                                    │
│ 3. Auto-login user                 │
│    - login(request, user)          │
│                                    │
│ 4. Redirect to dashboard           │
└────────────────────────────────────┘

Database effect:
User(role) ←OneToOne→ ProfileModel (e.g., PastorProfile)
member_id auto-generated: JBAC-PAS-123456 (for pastor)
```

---

## Search & Discovery Flow

```
┌──────────────────────────────────────────┐
│ User visits /directory/search/           │
├──────────────────────────────────────────┤
│ search_directory(request)                │
│ Shows search form + results grid         │
└──────────────────────────────────────────┘
              ▼
┌──────────────────────────────────────────┐
│ User submits filters:                    │
│ - type (all/pastor/church)               │
│ - query (text search)                    │
│ - district, state                        │
└──────────────────────────────────────────┘
              ▼
┌──────────────────────────────────────────┐
│ View executes queries:                   │
│                                          │
│ pastors = PastorProfile.objects.filter(  │
│   is_approved=True,                      │
│   is_public=True,                        │
│   district=filter_district               │
│ ).select_related('user')                 │
│                                          │
│ if query:                                │
│   .filter(pastor_name__icontains=q OR   │
│           church_name__icontains=q OR   │
│           user.mobile_number__i=q)      │
│                                          │
│ Limit to 24 results                      │
└──────────────────────────────────────────┘
              ▼
┌──────────────────────────────────────────┐
│ Map Search Alternative:                  │
│ /directory/map-search/                   │
│                                          │
│ Fetches churches with:                   │
│ - latitude/longitude (not null)          │
│ - is_approved & is_public                │
│ - Optional: district/state filters       │
│                                          │
│ Returns JSON markers:                    │
│ [{name, pastor, lat, lng, ...}, ...]     │
│                                          │
│ Frontend: Leaflet.js + OpenStreetMap     │
│ to render interactive map                │
└──────────────────────────────────────────┘

Note: BelieverProfile and StudentProfile
NOT searchable (confidentiality)
```

---

## Admin Approval Workflow

```
┌────────────────────────────────────────────────┐
│ User registers (e.g., PastorProfile)           │
├────────────────────────────────────────────────┤
│ On save:                                       │
│ - is_approved=False (default)                  │
│ - is_public=False (default)                    │
│ - NOT visible in search yet                    │
└────────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────────┐
│ Admin views /admin/directory/pastorprofile/    │
├────────────────────────────────────────────────┤
│ Sees list of pending profiles with:            │
│ - pastor_name, church_name, district           │
│ - is_approved, is_public checkboxes            │
│ - Filters by approval status                   │
└────────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────────┐
│ Admin clicks profile to view full details      │
├────────────────────────────────────────────────┤
│ - Verifies data accuracy                       │
│ - Checks GPS coordinates (if church)           │
│ - Reviews pastor credentials                   │
└────────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────────┐
│ Admin checks:                                  │
│ ☐ is_approved (enable searchability)          │
│ ☐ is_public (show in directory)               │
│                                                │
│ Or rejects/requests changes                    │
└────────────────────────────────────────────────┘
              ▼
┌────────────────────────────────────────────────┐
│ Admin clicks Save                              │
├────────────────────────────────────────────────┤
│ If is_approved=True AND is_public=True:        │
│ → Profile now searchable in                    │
│   /directory/search/ & /api/pastors/          │
│                                                │
│ If only is_approved=True:                      │
│ → Profile NOT searchable (private)             │
│                                                │
│ If both False:                                 │
│ → Profile pending or rejected                  │
└────────────────────────────────────────────────┘
```

---

## OTP Provider Configuration

```
┌─────────────────────────────────────────────┐
│ OTP_PROVIDER Environment Variable            │
├─────────────────────────────────────────────┤
│ Three options:                              │
└─────────────────────────────────────────────┘

1. CONSOLE (Default for development)
   ┌────────────────────────────────────────┐
   │ OTP_PROVIDER=console                   │
   │                                        │
   │ Code printed to Django console output  │
   │ DEV USE ONLY                           │
   │ Example: OTP Code: 123456              │
   └────────────────────────────────────────┘

2. TWILIO (for SMS)
   ┌────────────────────────────────────────┐
   │ OTP_PROVIDER=twilio                    │
   │ OTP_TWILIO_ACCOUNT_SID=AC...           │
   │ OTP_TWILIO_AUTH_TOKEN=...              │
   │ OTP_TWILIO_FROM_NUMBER=+1...           │
   │                                        │
   │ SMS sent via Twilio API                │
   │ User receives on phone                 │
   └────────────────────────────────────────┘

3. MSG91 (for SMS in India)
   ┌────────────────────────────────────────┐
   │ OTP_PROVIDER=msg91                     │
   │ OTP_MSG91_AUTH_KEY=...                 │
   │ OTP_MSG91_SENDER_ID=JBAC (optional)    │
   │ OTP_MSG91_TEMPLATE_ID=... (optional)   │
   │                                        │
   │ SMS sent via MSG91 API (India-focused) │
   │ Lowest cost for Indian numbers         │
   └────────────────────────────────────────┘

Fallback: If provider fails, console prints OTP
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────┐
│         Production Deployment Options            │
├──────────────────────────────────────────────────┤
│                                                  │
│ 1. PythonAnywhere (Hosted Python)               │
│    - pythonanywhere_wsgi.py configured          │
│    - SQLite or Neon PostgreSQL backend          │
│    - WhiteNoise serves static files             │
│    - Deployed at: rkarra.pythonanywhere.com     │
│                                                  │
│ 2. Render.com (Docker-based)                    │
│    - render.yaml defines build/start            │
│    - Container-based deployment                │
│    - Neon PostgreSQL external DB               │
│                                                  │
│ 3. Docker + Server (Custom hosting)             │
│    - Dockerfile for containerization           │
│    - Gunicorn WSGI server                       │
│    - Nginx reverse proxy (optional)             │
│    - PostgreSQL container (separate)            │
│                                                  │
│ 4. Generic WSGI (AWS, Azure, GCP)              │
│    - config/wsgi.py entry point                │
│    - Gunicorn server                           │
│    - Managed database service                  │
│                                                  │
└──────────────────────────────────────────────────┘

Static Files Strategy:
┌────────────────────────────────────────────────┐
│ Development:                                   │
│ - Django serves /static/ & /media/             │
│ - python manage.py collectstatic runs          │
│ - Files collected to /staticfiles/             │
│                                                │
│ Production:                                    │
│ - WhiteNoise middleware serves static files    │
│ - No need for separate web server config       │
│ - CompressedManifestStaticFilesStorage         │
│ - CSS/JS files fingerprinted (cache-busting)   │
└────────────────────────────────────────────────┘
```

---

## File Upload Paths

```
/media/
├── core/
│   └── about/
│       ├── image1.jpg (AboutPageContent.image)
│       └── document.pdf (AboutPageContent.pdf)
├── meetings/
│   └── posters/
│       ├── meeting_poster_1.jpg
│       └── event_flyer.pdf
└── updates/
    └── news/
        ├── article_image.jpg
        └── featured_photo.png

Configuration:
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT_ABSOLUTE = /workspaces/jbac.in/media/
```

---

## Cache & Performance

```
Songs Module (songs/views.py):
┌────────────────────────────────────────┐
│ _CACHE_TTL_SECONDS = 600 (10 minutes)  │
│ _BOOK_CACHE = {} (in-memory)           │
│                                        │
│ Caches Gutendex API responses          │
│ Fallback to hardcoded Christian books  │
│ if API unavailable                     │
└────────────────────────────────────────┘

Database Optimization:
┌────────────────────────────────────────┐
│ select_related('user') →                │
│ Joins User table (ForeignKey)           │
│                                        │
│ prefetch_related('items') →            │
│ Prefetches related NavigationItems      │
│                                        │
│ Result: Fewer database queries         │
└────────────────────────────────────────┘
```

---

## Security Measures

| Measure | Implementation |
|---------|-----------------|
| **Password Hashing** | Django default PBKDF2 + salt |
| **CSRF Protection** | CsrfViewMiddleware + {% csrf_token %} in forms |
| **XSS Prevention** | Template auto-escaping enabled |
| **SQL Injection** | Django ORM (parameterized queries) |
| **Rate Limiting** | OTP: 3 per 10 min, 30 min lockout after 5 fails |
| **HTTPS** | CSRF_TRUSTED_ORIGINS configured |
| **Session** | 2-week cookie expiration |
| **User Roles** | 8 roles with permission checks |
| **Mobile Auth** | Primary username (not email) |
| **IP Tracking** | OTPChallenge.request_ip stored |

---

## Quick Reference Tables

### User Roles
| Role | Description | Profile Model | Searchable |
|------|-------------|---------------|-----------|
| believer | Individual believer | BelieverProfile | No (private) |
| pastor | Church pastor | PastorProfile | Yes (if approved) |
| student | Christian student | StudentProfile | No (private) |
| church | Church organization | ChurchProfile | Yes (if approved) |
| pastor_association | Pastors' group | OrganizationProfile | Yes (if approved) |
| ministry | Ministry org | OrganizationProfile | Yes (if approved) |
| organization | Christian company | OrganizationProfile | Yes (if approved) |
| admin | System admin | N/A | Admin only |

### Districts (Andhra Pradesh)
28 districts supported: Visakhapatnam, Guntur, Krishna, Nellore, Kurnool, Srikakulam, Chittoor, East Godavari, West Godavari, Chittoor, Eluru, NTR, Kakinada, Tirupati, Vizianagaram, Prakasam, Bapatla, Alluri Sitharama Raju, Anakapalli, Anantapuramu, Annamayya, Dr. B.R. Ambedkar Konaseema, Palnadu, Parvathipuram Manyam, Sri Sathya Sai, Sri Potti Sriramulu Nellore, YSR Kadapa, Nandyal

### News Categories
| Category | Purpose |
|----------|---------|
| christian-media | Christian media news |
| honorarium | Govt schemes, stipends |
| christians | General Christian news |
| general | Miscellaneous |
| medical-council | Delhi Medical Council |
| education | Education-related |
| training | Training programs |
| jobs | Job opportunities |
| health | Health/wellness |
| society | Social issues |
| dr-joseph | About Dr. Joseph Prakash Mosiganti |

---

## Common Admin Tasks

### Approve a Pastor Profile
1. Go to `/admin/directory/pastorprofile/`
2. Click on pastor name
3. Check `is_approved` ✓
4. Check `is_public` ✓
5. Click Save
6. Profile now searchable at `/directory/search/`

### Publish News Article
1. Go to `/admin/updates/newsarticle/`
2. Click on article title
3. Check `is_published` ✓
4. Check `is_featured` ✓ (optional, for homepage)
5. Set `published_at` to current date/time
6. Click Save
7. Article visible at `/news/`

### Create Custom Navigation Menu
1. Go to `/admin/core/navigationgroup/`
2. Add new NavigationGroup
   - slug: "custom-menu"
   - title_en: "Custom Menu"
   - title_te: "కస్టమ్ మెను"
3. Save
4. Go to NavigationItem and add items to group
5. Items appear in site navigation

### Create About Page Section
1. Go to `/admin/core/aboutpagecontent/`
2. Add new AboutPageContent
   - section_slug: "about-ministry"
   - menu_title_en/te: Display names
   - page_title_en/te: Page heading
   - description: Content (supports HTML)
   - youtube_embed_url: (optional) YouTube video
   - image: (optional) Upload image
   - pdf: (optional) Upload PDF
   - sort_order: Display order
   - is_active: Enable/disable
3. Save
4. Section appears at `/about-us/about-ministry/`

---

## Troubleshooting Matrix

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| OTP not sending | OTP_PROVIDER not configured | Set OTP_PROVIDER=console (for dev) |
| Profile not searchable | is_approved or is_public unchecked | Go to admin, check both boxes |
| Static files missing | collectstatic not run | `python manage.py collectstatic --noinput` |
| Login fails | Wrong role selected | Ensure registered role matches login role |
| Map not loading | Churches have no lat/long | Update church profile with coordinates |
| News doesn't appear | is_published unchecked | Go to admin, check is_published |
| Page 500 error | Migration not run | `python manage.py migrate` |
| Database locked | SQLite concurrency issue | Use PostgreSQL in production |

---

## Next Steps for Replication

1. **Create project structure** (see CONFIGURATION_REFERENCE.md)
2. **Copy all code** from this repository:
   - Models
   - Views
   - Forms
   - URLs
   - Templates
   - Admin configs
3. **Run migrations**: `python manage.py migrate`
4. **Create admin user**: `python manage.py createsuperuser`
5. **Configure OTP** (optional)
6. **Load fixtures** (AboutPageContent, Navigation)
7. **Test locally**: `python manage.py runserver`
8. **Deploy** to production server

---

## Resources

- **Django Docs**: https://docs.djangoproject.com/
- **PostgreSQL**: https://www.postgresql.org/
- **Neon (Managed PostgreSQL)**: https://neon.tech/
- **Leaflet Maps**: https://leafletjs.com/
- **ReportLab (PDF)**: https://www.reportlab.com/
- **Twilio (SMS)**: https://www.twilio.com/
- **MSG91 (SMS India)**: https://msg91.com/

---

**Generated**: 2026-05-18  
**Repository**: https://github.com/r-karra/jbac_core  
**Status**: Complete & Production-Ready

