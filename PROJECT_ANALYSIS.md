# JBAC (Jesus Believers Association Council) - Comprehensive Project Analysis

**Project URL**: https://github.com/r-karra/jbac_core

**Technology Stack**: Django 5.1.15, Python 3.12+, SQLite/PostgreSQL, Bilingual (Telugu/English)

---

## 1. PROJECT OVERVIEW

JBAC is a Django-based community platform designed for Christians in Andhra Pradesh and Telangana. It provides:
- Secure, role-based registrations for believers, pastors, students, churches, and organizations
- Searchable pastor and church directory with geographic filtering
- News/announcements publishing system
- Meeting scheduling and discovery
- Songs/hymns library
- PDF member ID card generation
- Admin dashboard for approval workflows
- JSON APIs for external integration

---

## 2. DATABASE MODELS

### 2.1 ACCOUNTS App (`accounts/models.py`)

#### **User Model** (extends AbstractUser)
- **Fields**:
  - `username`: Removed (replaced with `mobile_number`)
  - `mobile_number` (CharField, 20, unique) - Primary authentication field
  - `email` (EmailField, unique, nullable)
  - `role` (CharField with choices) - One of: believer, pastor, student, pastor_association, ministry, church, organization, admin
  - `member_id` (CharField, 24, unique, auto-generated) - Format: `JBAC-{ROLE_PREFIX}-{RANDOM_6_DIGITS}`
  - `preferred_language` (CharField) - 'en' (English) or 'te' (Telugu), default='en'
  - `confidentiality_acknowledged` (Boolean) - User consent for data storage
- **Authentication**: Uses mobile number as USERNAME_FIELD instead of username
- **Methods**:
  - `display_name()` - Returns full name or mobile number
  - `get_role_display()` - Role label
- **Manager**: Custom UserManager with `_create_user()`, `create_user()`, `create_superuser()` methods

#### **OTPChallenge Model**
- **Purpose**: Handles OTP-based authentication flow
- **Fields**:
  - `user` (ForeignKey to User) - User attempting login
  - `role` (CharField) - Selected role at OTP request
  - `identifier` (CharField, 120) - Mobile number or email used for OTP
  - `request_ip` (GenericIPAddressField) - IP address of requester
  - `code` (CharField, 6) - 6-digit OTP code
  - `expires_at` (DateTimeField) - OTP expiration time (10 minutes)
  - `failed_attempts` (PositiveSmallIntegerField) - Failed verification attempts
  - `locked_until` (DateTimeField, nullable) - Lockout time after max failed attempts
  - `is_used` (Boolean) - Marks OTP as consumed after successful verification
  - `created_at` (DateTimeField) - Creation timestamp
- **Methods**:
  - `is_valid()` - Returns True if not used, not locked, and not expired
  - `is_locked()` - Returns True if currently locked

---

### 2.2 DIRECTORY App (`directory/models.py`)

#### **ApprovalFields** (Abstract Base Model)
- **Purpose**: Shared fields for all profile models
- **Fields**:
  - `is_approved` (Boolean) - Admin approval status
  - `is_public` (Boolean) - Whether visible in search/directory
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)

#### **BelieverProfile**
- Extends: ApprovalFields
- **Fields**:
  - `user` (OneToOneField to User)
  - `full_name` (CharField, 200)
  - `gender` (CharField) - male, female, other
  - `whatsapp_number` (CharField, 20)
  - `date_of_birth` (DateField, nullable)
  - `life_goal` (TextField)
  - `hobbies` (TextField)
  - `youtube_channel` (URLField)
  - `additional_information` (TextField)

#### **PastorProfile**
- Extends: ApprovalFields
- **Fields**:
  - `user` (OneToOneField to User)
  - `pastor_name` (CharField, 200)
  - `gender` (CharField) - male, female, other
  - `church_name` (CharField, 200)
  - `church_address` (TextField)
  - `district` (CharField) - Dropdown of Andhra Pradesh districts (28 options)
  - `state` (CharField) - Andhra Pradesh, Telangana, Other
  - `latitude` (DecimalField) - Church location latitude
  - `longitude` (DecimalField) - Church location longitude
  - `years_of_ministry` (PositiveIntegerField)
  - `additional_information` (TextField)
- **Ordering**: by pastor_name

#### **StudentProfile**
- Extends: ApprovalFields
- **Fields**:
  - `user` (OneToOneField to User)
  - `student_name` (CharField, 200)
  - `gender` (CharField)
  - `college_name` (CharField, 200)
  - `course` (CharField, 200)
  - `year_of_study` (CharField, 100)
  - `district` (CharField) - AP districts
  - `state` (CharField)

#### **ChurchProfile**
- Extends: ApprovalFields
- **Fields**:
  - `user` (OneToOneField to User)
  - `church_name` (CharField, 200)
  - `pastor_name` (CharField, 200)
  - `address` (TextField)
  - `village` (CharField, 200)
  - `district` (CharField) - AP districts
  - `state` (CharField)
  - `latitude` (DecimalField)
  - `longitude` (DecimalField)
  - `year_established` (PositiveIntegerField, nullable)
  - `ministry_details` (TextField)
- **Ordering**: by church_name

#### **OrganizationProfile**
- Extends: ApprovalFields
- **Fields**:
  - `user` (OneToOneField to User)
  - `organization_name` (CharField, 200)
  - `founder_name` (CharField, 200)
  - `address` (TextField)
  - `district` (CharField)
  - `state` (CharField)
  - `website` (URLField)
  - `ministry_type` (CharField, 200)
- **Ordering**: by organization_name

#### **Helper Function**: `get_profile_for_user(user)`
- Returns appropriate profile based on user role
- Mapping: believer→believer_profile, pastor→pastor_profile, student→student_profile, church→church_profile, pastor_association/ministry/organization→organization_profile

---

### 2.3 UPDATES App (`updates/models.py`)

#### **NewsArticle**
- **Purpose**: Content management for news and announcements
- **Fields**:
  - `title` (CharField, 300)
  - `slug` (SlugField, 320, unique, auto-generated from title)
  - `image` (ImageField) - Upload path: 'updates/news/'
  - `image_url` (URLField) - Alternative to uploaded image
  - `youtube_embed_url` (URLField)
  - `summary` (TextField)
  - `content` (TextField) - Main article content
  - `newspaper` (CharField) - Source: andhra-jyothi, eenadu, sakshi, deccan-chronicle, the-hindu, times-of-india, indian-express, other
  - `category` (CharField) - Options: christian-media, honorarium, christians, general, medical-council, education, training, jobs, health, society, dr-joseph
  - `published_at` (DateTimeField)
  - `is_published` (Boolean) - Controls visibility
  - `is_featured` (Boolean) - Highlighted on homepage
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
- **Ordering**: by -published_at, -created_at
- **Methods**:
  - `display_image_url()` - Returns image.url or image_url
- **Auto-generation**: Slug auto-generated on save if not provided

---

### 2.4 MEETINGS App (`meetings/models.py`)

#### **Meeting**
- **Purpose**: Event scheduling and discovery
- **Fields**:
  - `title` (CharField, 220)
  - `description` (TextField)
  - `start_date` (DateField)
  - `end_date` (DateField)
  - `organizer_name` (CharField, 180)
  - `estimated_attendance` (PositiveIntegerField)
  - `organizer_phone` (CharField, 20)
  - `address` (TextField)
  - `district` (CharField) - 21 AP/Telangana districts
  - `state` (CharField)
  - `city_area` (CharField, 120, optional)
  - `mandal` (CharField, 120, optional) - Administrative subdivision
  - `village` (CharField, 120, optional)
  - `meeting_type` (CharField) - vbs, revival (ఉద్ధీపన సమావేశాలు), gospel (సువార్త సమావేశాలు), youth (యూత్ మీటింగ్‌లు), leaders (క్రైస్తవ నాయకుల సమావేశాలు)
  - `denomination` (CharField) - Assembly of God, Baptist, Bible Mission, Brethren, Church of Christ, CSI, Pentecost, Catholics
  - `ministry` (CharField) - 8 major ministry organizations
  - `google_map_location` (URLField)
  - `latitude` (DecimalField)
  - `longitude` (DecimalField)
  - `poster` (FileField) - Upload path: 'meetings/posters/'
  - `youtube_link` (URLField)
  - `additional_info` (TextField)
  - `is_published` (Boolean) - Visibility control
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
- **Ordering**: by start_date, title

---

### 2.5 CORE App (`core/models.py`)

#### **AboutPageContent**
- **Purpose**: Customizable "About Us" page sections via admin
- **Fields**:
  - `section_slug` (SlugField, 80, unique) - Identifier
  - `menu_title_te` (CharField, 200) - Telugu menu label
  - `menu_title_en` (CharField, 200) - English menu label
  - `page_title_te` (CharField, 200) - Telugu page title
  - `page_title_en` (CharField, 200) - English page title
  - `description` (TextField) - Section content
  - `points_text` (TextField) - Bullet points (one per line)
  - `youtube_embed_url` (URLField) - Parses youtu.be and youtube.com URLs
  - `image` (ImageField) - Upload path: 'core/about/'
  - `pdf` (FileField) - Upload path: 'core/about/'
  - `sort_order` (PositiveSmallIntegerField, default=10)
  - `is_active` (Boolean)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
- **Ordering**: by sort_order, menu_title_en
- **Methods**:
  - `points()` - Parses and returns bullet points as list
  - `youtube_embed_src()` - Extracts video ID and returns embed URL

#### **NavigationGroup**
- **Purpose**: Custom navigation menu sections
- **Fields**:
  - `slug` (SlugField, 80, unique)
  - `title_te` (CharField, 200)
  - `title_en` (CharField, 200)
  - `prompt_title_te` (CharField, 200) - Unauthenticated user prompt title
  - `prompt_title_en` (CharField, 200)
  - `prompt_message_te` (TextField)
  - `prompt_message_en` (TextField)
  - `sort_order` (PositiveSmallIntegerField, default=10)
  - `is_active` (Boolean)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
- **Ordering**: by sort_order, title_en
- **Methods**:
  - `display_title()`, `prompt_title()`, `prompt_message()`

#### **NavigationItem**
- **Purpose**: Menu items within navigation groups
- **Fields**:
  - `group` (ForeignKey to NavigationGroup) - Parent group
  - `title_te` (CharField, 200)
  - `title_en` (CharField, 200)
  - `url_name` (CharField, 200) - Django URL name (for reverse lookup)
  - `url_kwargs` (JSONField) - URL parameters as JSON dict
  - `url_path` (CharField, 255) - Direct path (takes precedence over url_name)
  - `sort_order` (PositiveSmallIntegerField, default=10)
  - `is_active` (Boolean)
  - `requires_auth` (Boolean) - Show only when authenticated
  - `staff_only` (Boolean) - Show only for staff members
  - `open_in_new_tab` (Boolean)
  - `created_at` (DateTimeField, auto_now_add)
  - `updated_at` (DateTimeField, auto_now)
- **Ordering**: by sort_order, title_en
- **Methods**:
  - `display_title()` - Returns Telugu or English title
  - `href()` - Resolves URL using url_name/url_kwargs or url_path

---

## 3. VIEWS

### 3.1 ACCOUNTS App (`accounts/views.py`)

#### **LoginView** (Class-based View)
- **Template**: `accounts/login.html`
- **GET**: Renders login form
- **POST**: Authenticates via password login
- **Logic**: Uses custom `LoginForm` for role-based authentication
- **Redirect on success**: `core:dashboard`

#### **OTPRequestView** (Class-based View)
- **Template**: `accounts/otp_request.html`
- **GET**: Renders OTP request form
- **POST**: 
  - Validates identifier (mobile/email) and role
  - Implements rate limiting: max 3 OTP requests per 10 minutes
  - Generates 6-digit random code
  - Calls `send_otp_code()` to deliver via SMS/email
  - Stores OTP challenge in session
- **Redirect on success**: `accounts:otp-verify`

#### **OTPVerifyView** (Class-based View)
- **Template**: `accounts/otp_verify.html`
- **GET**: Renders OTP verification form
- **POST**:
  - Validates OTP code
  - Implements lockout: max 5 failed attempts (locked for 30 minutes)
  - Marks OTP as used after success
  - Logs in user via ModelBackend
- **Redirect on success**: `core:dashboard`

#### **logout_view** (Function-based)
- Logs out authenticated user
- **Redirect**: `core:home`

---

### 3.2 CORE App (`core/views.py`)

#### **home** (Function-based)
- **Template**: `core/home.html`
- **Context**:
  - `stats`: Profile counts (believers, pastors, students, churches, organizations)
  - `featured_articles`: Top 3 featured news items
  - `latest_articles`: Top 4 latest news items

#### **about** (Function-based)
- **Template**: `core/about.html`
- Simple static page

#### **about_subpage** (Function-based)
- **Template**: `core/about_subpage.html`
- **Parameter**: `section` (slug)
- **Logic**: 
  - Fetches AboutPageContent from admin (if exists) or uses hardcoded ABOUT_SECTIONS
  - Falls back to default if no admin content
  - Generates menu items with active state

#### **navigation_group_page** (Function-based)
- **Template**: `core/navigation_group.html`
- **Parameter**: `slug` (NavigationGroup slug)
- **Logic**:
  - Filters items by auth status and staff status
  - Shows prompt to unauthenticated users
  - **Decorators**: Requires group to be active

---

### 3.3 DIRECTORY App (`directory/views.py`)

#### **registration_landing** (Function-based)
- **Template**: `directory/register_landing.html`
- Lists all 5 registration categories (believer, pastor, student, church, organization)

#### **register_category** (Function-based)
- **Template**: `directory/registration_form.html`
- **Parameter**: `category` (slug)
- **POST**:
  - Saves profile and creates associated User
  - Logs in user automatically
  - **Redirect**: `core:dashboard`

#### **search_directory** (Function-based)
- **Template**: `directory/search.html`
- **Query Parameters**: 
  - `type` (all, pastor, church)
  - `query` (text search)
  - `district`, `state`
- **Logic**:
  - Filters approved, public profiles
  - Full-text search on name, church/organization, phone
  - Limits results to 24 items
- **Note**: Does NOT search believer or student profiles (confidentiality)

#### **map_search** (Function-based)
- **Template**: `directory/map_search.html`
- **Query Parameters**: `district`, `state`
- **Logic**:
  - Fetches churches with coordinates (latitude/longitude)
  - Returns JSON markers for map visualization
  - Uses predefined district center points for zoom
  - Limit: 200 churches per request

#### **member_id_pdf** (Function-based)
- **Decorator**: `@login_required`
- **Logic**: Generates A6 PDF (greeting card size) with member details
- **Response**: PDF download
- **Design**: Dark green background (#163126) with white text

---

### 3.4 UPDATES App (`updates/views.py`)

#### **news_list** (Function-based)
- **Template**: `updates/news_list.html`
- Displays published articles ordered by -published_at

#### **news_detail** (Function-based)
- **Template**: `updates/news_detail.html`
- **Parameter**: `slug`
- Shows article + 3 related articles

#### **submit_news** (Function-based)
- **Template**: `updates/submit_news.html`
- **Decorator**: `@login_required`
- **POST**: 
  - Saves NewsArticle
  - Respects `AUTO_PUBLISH_USER_NEWS` env var
  - If False: awaits admin approval
  - If True: publishes immediately

---

### 3.5 MEETINGS App (`meetings/views.py`)

#### **submit_meeting** (Function-based)
- **Template**: `meetings/submit_meeting.html`
- **Decorator**: `@login_required`
- **POST**: Saves Meeting with is_published=True

#### **view_meetings** (Function-based)
- **Template**: `meetings/view_meetings.html`
- **Query Parameters**:
  - `meeting_type`, `denomination`, `ministry`
  - `date`, `district`
  - `city_area`, `mandal`, `village`
  - `location` (text search)
- **Logic**: Filters published, future meetings only

#### **meeting_detail** (Function-based)
- **Template**: `meetings/meeting_detail.html`
- Shows meeting details

---

### 3.6 API Views (`api/views.py`)

#### **platform_stats_api** (GET)
- **Endpoint**: `/api/stats/`
- **Response**: JSON with profile counts

#### **pastors_api** (GET)
- **Endpoint**: `/api/pastors/`
- **Parameters**: `q` (search), `district`, `state`
- **Response**: JSON array of approved, public pastors (max 100)

#### **churches_api** (GET)
- **Endpoint**: `/api/churches/`
- **Parameters**: `q`, `district`, `state`
- **Response**: JSON array of churches with coordinates

#### **news_api** (GET)
- **Endpoint**: `/api/news/`
- **Response**: JSON array of published articles (max 30)

---

### 3.7 SONGS App (`songs/views.py`)

#### **songs_search** (Function-based)
- **Template**: `songs/search.html`
- **Features**:
  - Fetches from external API (Rejoice In Lord public songs DB)
  - Filters by category (telugu, hymns, choruses)
  - Paginated results (24 items per page)
  - Fallback to empty results if service unavailable

#### **books_list** (Function-based)
- **Features**:
  - Fetches from Gutendex API (free books)
  - Fallback to hardcoded Christian books
  - 6-month caching

---

## 4. FORMS

### 4.1 ACCOUNTS App (`accounts/forms.py`)

#### **StyledFormMixin**
- Adds CSS classes to form widgets automatically
- Classes: `form-input`, `form-checkbox`, `form-select`, `form-textarea`

#### **LoginForm**
- **Fields**: `role`, `identifier` (mobile/email), `password`
- **Validation**: Custom backend authentication
- **Labels**: Telugu

#### **OTPRequestForm**
- **Fields**: `role`, `identifier`
- **Validation**: Finds user by (mobile OR email) AND role

#### **OTPVerifyForm**
- **Fields**: `code` (6-digit)

---

### 4.2 DIRECTORY App (`directory/forms.py`)

#### **BaseRegistrationForm**
- Extends: StyledFormMixin, ModelForm
- **Base Fields**:
  - `mobile_number` (CharField, unique validation)
  - `email` (EmailField, optional, unique validation)
  - `password1`, `password2` (PasswordFields, matched validation)
  - `consent` (BooleanField, required)
- **Methods**:
  - `build_user_kwargs()` - Prepares User creation params
  - `save()` - Creates User + Profile atomically

#### **BelieverRegistrationForm**
- **Model**: BelieverProfile
- **Role**: believer
- **Additional Fields**: full_name, gender, whatsapp_number, date_of_birth, life_goal, hobbies, youtube_channel, additional_information

#### **PastorRegistrationForm**
- **Model**: PastorProfile
- **Role**: pastor
- **Additional Fields**: pastor_name, gender, church_name, church_address, district, state, latitude, longitude, years_of_ministry, additional_information

#### **StudentRegistrationForm**
- **Model**: StudentProfile
- **Role**: student
- **Fields**: student_name, gender, college_name, course, year_of_study, district, state

#### **ChurchRegistrationForm**
- **Model**: ChurchProfile
- **Role**: church
- **Fields**: church_name, pastor_name, address, village, district, state, latitude, longitude, year_established, ministry_details

#### **OrganizationRegistrationForm**
- **Model**: OrganizationProfile
- **Role**: Selector (pastor_association, ministry, organization)
- **Fields**: organization_name, founder_name, address, district, state, website, ministry_type

---

### 4.3 MEETINGS App (`meetings/forms.py`)

#### **MeetingSubmissionForm**
- **Model**: Meeting
- **Fields**: All 22 fields from Meeting model
- **Validation**: end_date >= start_date
- **All dropdowns**: Pre-populated with proper choices

#### **MeetingFilterForm**
- **Fields**: meeting_type, denomination, ministry, date, district, city_area, mandal, village
- **All optional**

---

### 4.4 UPDATES App (`updates/forms.py`)

#### **NewsSubmissionForm**
- **Model**: NewsArticle
- **Fields**: title, image, newspaper (optional), category (required), summary, content
- **Visible for**: Logged-in users

#### **NewsAdminForm**
- **Model**: NewsArticle
- **Fields**: All including image_url, youtube_embed_url, is_published, is_featured, published_at
- **Visible for**: Admin only

---

## 5. TEMPLATES/PAGES

### 5.1 Base Templates

#### **base.html**
- **Features**:
  - Responsive header with dropdown navigation
  - Mobile menu toggle button
  - Bilingual language switcher (Telugu/English)
  - Message display section
  - Footer with quick links, social media, contact
  - Google Translate integration
- **Navigation Groups**: Dynamically loaded from DB
- **Submenu**: Shows/hides based on authentication status and role

---

### 5.2 Core App Templates

#### **core/home.html**
- **Sections**:
  - Hero banner with registration CTA
  - Service cards (Directory, Updates)
  - Author bio section (Prof. Dr. Joseph P. Mosiganti)
  - Featured news grid
  - Registration CTA

#### **core/about.html**
- Static about page

#### **core/about_subpage.html**
- **Sidebar menu**: All about sections
- **Main content**: Dynamic section with image, PDF, embedded video, bullet points

#### **core/navigation_group.html**
- Shows menu items from NavigationGroup
- Unauthenticated users see prompt

#### **core/contact.html**
- Contact information and form

#### **core/dashboard.html**
- User profile summary
- Role-specific content
- Links to member ID, edit profile, etc.

#### **core/admin_dashboard.html**
- Admin stats
- Pending approval counts
- Management quick links

---

### 5.3 Accounts Templates

#### **accounts/login.html**
- Login form with role dropdown
- Link to OTP login

#### **accounts/otp_request.html**
- OTP request form
- Info card explaining OTP flow
- Link back to password login

#### **accounts/otp_verify.html**
- OTP code input (6 digits)
- Challenge details display
- Remaining attempts indicator

---

### 5.4 Directory Templates

#### **directory/register_landing.html**
- 5 registration cards with descriptions
- Direct links to each registration form

#### **directory/registration_form.html**
- Dynamic form for selected category
- Category name + description at top
- All form fields with Telugu labels
- Submit button

#### **directory/search.html**
- Search form with filters (query, district, state, type)
- Results grid showing pastor/church cards
- Search parameters are sticky

#### **directory/map_search.html**
- District selector dropdown
- Leaflet map with OpenStreetMap tiles
- Church markers with tooltips
- Sidebar with church list

---

### 5.5 Updates Templates

#### **updates/news_list.html**
- Grid of news cards
- Each card shows: date, title, summary, read more link
- Ordered by -published_at

#### **updates/news_detail.html**
- Full article content
- Featured image or YouTube embed
- Related articles (3) at bottom

#### **updates/submit_news.html**
- News submission form
- Visible only to authenticated users

---

### 5.6 Meetings Templates

#### **meetings/submit_meeting.html**
- Meeting submission form with all 22 fields
- Date pickers, location fields
- Poster upload
- YouTube link field

#### **meetings/view_meetings.html**
- Filter form (meeting_type, denomination, ministry, date, location)
- Filtered meetings list
- Each meeting shows: date, title, location, organizer

#### **meetings/meeting_detail.html**
- Full meeting details
- Location map (if coordinates provided)
- YouTube link (if provided)

---

### 5.7 Songs Templates

#### **songs/search.html**
- Search form with category dropdown
- Results grouped by category
- Pagination controls
- Service status messages

#### **songs/books.html**
- Christian books list
- Filtered from Gutendex API
- Book covers, authors, download counts

---

## 6. URL PATTERNS

### 6.1 Root Configuration (`config/urls.py`)

```
/admin/ → Django Admin
/ → core.urls
/accounts/ → accounts.urls
/directory/ → directory.urls
/news/ → updates.urls
/meetings/ → meetings.urls
/songs/ → songs.urls
/api/ → api.urls
```

### 6.2 Core URLs (`core/urls.py`)

| Path | Name | View | Purpose |
|------|------|------|---------|
| / | home | home | Homepage |
| about/ | about | about | About page |
| about-us/ | about-us | about_subpage | About landing |
| about-us/<slug:section>/ | about-section | about_subpage | About section detail |
| menu/<slug:slug>/ | navigation-group | navigation_group_page | Dynamic navigation section |
| contact/ | contact | contact | Contact page |
| privacy-policy/ | privacy-policy | privacy_policy | Privacy policy |
| terms-and-conditions/ | terms-and-conditions | terms_conditions | Terms & conditions |
| dashboard/ | dashboard | dashboard | User dashboard |
| admin-dashboard/ | admin-dashboard | admin_dashboard | Admin dashboard |

### 6.3 Accounts URLs (`accounts/urls.py`)

| Path | Name | View | Purpose |
|------|------|------|---------|
| login/ | login | LoginView.as_view() | Password login |
| otp/ | otp-request | OTPRequestView.as_view() | OTP request |
| otp/verify/ | otp-verify | OTPVerifyView.as_view() | OTP verification |
| logout/ | logout | logout_view | Logout |

### 6.4 Directory URLs (`directory/urls.py`)

| Path | Name | View | Purpose |
|------|------|------|---------|
| register/ | register | registration_landing | Registration options |
| register/<slug:category>/ | register-category | register_category | Registration form for category |
| search/ | search | search_directory | Directory search |
| map-search/ | map-search | map_search | Geographic search |
| member-id/ | member-id | member_id_pdf | PDF member ID download |

### 6.5 Updates URLs (`updates/urls.py`)

| Path | Name | View | Purpose |
|------|------|------|---------|
| | list | news_list | News listing |
| submit/ | submit | submit_news | Submit news |
| <slug:slug>/ | detail | news_detail | Article detail |

### 6.6 Meetings URLs (`meetings/urls.py`)

| Path | Name | View | Purpose |
|------|------|------|---------|
| | (redirect) | view | Redirects to /view/ |
| submit/ | submit | submit_meeting | Submit meeting |
| view/ | view | view_meetings | View meetings |
| view/<int:meeting_id>/ | detail | meeting_detail | Meeting detail |

### 6.7 API URLs (`api/urls.py`)

| Path | Name | View | Purpose |
|------|------|------|---------|
| stats/ | stats | platform_stats_api | Aggregate counts |
| pastors/ | pastors | pastors_api | Pastor search API |
| churches/ | churches | churches_api | Church search API |
| news/ | news | news_api | News feed API |

### 6.8 Songs URLs (`songs/urls.py`)

| Path | Name | View | Purpose |
|------|------|------|---------|
| | search | songs_search | Song search |
| books/ | books | books_list | Christian books |
| view/ | detail | song_detail | Song detail |
| <slug:category>/ | category | songs_search | Category-specific search |

---

## 7. KEY FEATURES BY APP

### 7.1 ACCOUNTS App - Authentication & User Management

**Features**:
- Multi-role authentication (8 roles)
- Dual authentication: Password-based or OTP-based
- OTP via SMS/Email/Console (configurable)
- Member ID generation (auto-formatted)
- Bilingual interface (English/Telugu)
- Confidentiality acknowledgment requirement
- Login attempt rate limiting
- Failed OTP lockout (30 minutes after 5 attempts)

**Security**:
- Mobile number-based USERNAME_FIELD
- Request IP tracking
- OTP expiration (10 minutes)
- Failed attempt tracking
- Password hashing via Django's default

---

### 7.2 DIRECTORY App - Profiles & Search

**Features**:
- 5 profile types (Believer, Pastor, Student, Church, Organization)
- Role-based registration flows
- Profile approval workflow (admin verification)
- Public/Private visibility toggle
- Geographic filtering (district, state)
- Full-text search on name, phone, email
- Searchable pastor/church directory (NOT believer/student - confidentiality)
- District map search with Leaflet.js + OpenStreetMap
- Coordinate-based church location visualization
- Member ID PDF generation (A6 card format)

**Admin Workflow**:
- Dashboard shows pending approvals
- Bulk publish/unpublish actions

---

### 7.3 UPDATES App - News & Announcements

**Features**:
- Admin publishing (editorial control)
- User submissions (configurable auto-publish or moderation)
- Categorized news (11 categories)
- Featured articles carousel
- Image/URL support
- YouTube embed support
- Newspaper attribution
- Slug-based URLs (SEO-friendly)

---

### 7.4 MEETINGS App - Event Management

**Features**:
- Meeting submission form (22 fields)
- Rich location data (address, district, mandal, village, coordinates)
- Meeting types (5 types)
- Denomination/Ministry filtering
- Future meetings only (via end_date >= today)
- Multi-field filtering (type, denomination, location, date)
- Poster upload
- YouTube link support
- Meeting detail view

---

### 7.5 CORE App - Navigation & Content

**Features**:
- Dynamic about page (configurable via admin)
- Fallback to hardcoded content
- YouTube embed parsing (3 URL formats supported)
- Navigation menu builder (custom menu items)
- Authentication-based menu visibility
- Staff-only menu items
- Bilingual menu labels
- Contact/Privacy/Terms pages
- User dashboard
- Admin dashboard with statistics

---

### 7.6 SONGS App - Library & Resources

**Features**:
- Song search (external API: Rejoice In Lord)
- Categories: Telugu, Hymns, Choruses
- Pagination (24 items per page)
- Fallback to empty results
- Christian books search (Gutendex API)
- 6-month caching
- Fallback to hardcoded Christian books list

---

### 7.7 API App - Integration

**Features**:
- Platform statistics (counts)
- Searchable pastor API
- Searchable church API with coordinates
- News feed API
- JSON responses
- Query-based filtering
- Rate-limited (implicit via query limits)

---

## 8. INSTALLED APPS

```python
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
```

---

## 9. MIDDLEWARE & CONFIGURATION

**Middleware Stack**:
- SecurityMiddleware
- WhiteNoiseMiddleware (static file serving)
- SessionMiddleware
- CommonMiddleware
- CsrfViewMiddleware
- AuthenticationMiddleware
- MessageMiddleware
- XFrameOptionsMiddleware

**Authentication Backend**: Custom backend in `config/auth_backends.py` (role-based, mobile/email hybrid)

**Database**: SQLite (development) or PostgreSQL via Neon (production)

**Static Files**: Collected via WhiteNoise, using `site.css` and `site.js`

**Media Files**: Served from `/media/` (development only)

---

## 10. ENVIRONMENT VARIABLES

| Variable | Purpose | Default |
|----------|---------|---------|
| SECRET_KEY | Django secret | jbac-development-secret-key |
| DEBUG | Debug mode | True |
| ALLOWED_HOSTS | Allowed domains | 127.0.0.1,localhost |
| DATABASE_URL | DB connection | SQLite (db.sqlite3) |
| OTP_PROVIDER | SMS provider | console |
| OTP_TWILIO_ACCOUNT_SID | Twilio config | - |
| AUTO_PUBLISH_USER_NEWS | Auto-publish submissions | True |

---

## 11. DEPLOYMENT

**Supported Platforms**:
- PythonAnywhere (configured in pythonanywhere_wsgi.py)
- Render (render.yaml)
- Docker (Dockerfile)
- Generic WSGI (gunicorn)

**Database**:
- Development: SQLite
- Production: Neon PostgreSQL

---

## 12. TECHNOLOGY STACK

- **Framework**: Django 5.1.15
- **Python**: 3.12+
- **Database**: SQLite/PostgreSQL
- **Static Files**: WhiteNoise
- **Server**: Gunicorn
- **Frontend**: Vanilla JavaScript, Leaflet.js, OpenStreetMap
- **PDF Generation**: ReportLab
- **Image Processing**: Pillow
- **OTP Providers**: Twilio, MSG91, Console
- **External APIs**: Rejoice In Lord (songs), Gutendex (books), Google Translate

---

## 13. CREATING A REPLICA

### To replicate this project in another workspace:

1. **Create Django project structure**:
   ```
   django-admin startproject config .
   python manage.py startapp core
   python manage.py startapp accounts
   python manage.py startapp directory
   python manage.py startapp updates
   python manage.py startapp api
   python manage.py startapp meetings
   python manage.py startapp songs
   ```

2. **Copy all models** from each app's `models.py`

3. **Copy all forms** from `forms.py` files

4. **Copy all views** from `views.py` files

5. **Set up URLs** as per section 6

6. **Copy templates** from `/templates` directory

7. **Configure settings.py**:
   - Add all INSTALLED_APPS
   - Configure AUTHENTICATION_BACKENDS
   - Set up MEDIA/STATIC files
   - Configure OTP_PROVIDER

8. **Copy admin.py** configurations for each app

9. **Run migrations**:
   ```
   python manage.py migrate
   python manage.py createsuperuser
   ```

10. **Collect static files**:
    ```
    python manage.py collectstatic --noinput
    ```

11. **Load fixtures** (if available) for AboutPageContent, NavigationGroups

12. **Test locally**:
    ```
    python manage.py runserver
    ```

---

## 14. AUTHENTICATION FLOW

### Password Login:
1. User selects role → enters mobile/email → password
2. Custom backend validates credentials
3. User redirected to dashboard

### OTP Login:
1. User selects role → enters mobile/email
2. Rate limit checked (max 3 per 10 minutes)
3. OTP code generated (6 digits)
4. Code sent via configured OTP provider
5. User enters OTP (6 digits)
6. Validation: not used, not locked, not expired
7. Failed attempt tracking (max 5, lock for 30 min)
8. Success: OTP marked used, user logged in

---

## 15. ADMIN PANEL CUSTOMIZATION

All models registered in admin with:
- **List displays**: Key fields for quick overview
- **Filters**: By approval status, district, category, date
- **Search fields**: Name, phone, email, identifiers
- **Inline edits**: NavigationItems within Groups
- **Custom actions**: Publish/unpublish meetings
- **Fieldsets**: Organized into logical sections
- **Readonly fields**: Timestamps, auto-generated IDs

---

**Document Generated**: 2026-05-18

**Project URL**: https://github.com/r-karra/jbac_core

This comprehensive analysis includes all models, views, forms, URL patterns, templates, and features across the entire JBAC project and can be used as a complete reference for replication in another workspace.
