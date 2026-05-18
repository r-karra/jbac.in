# Angular Frontend Application Analysis
## JBAC Core Frontend (r-karra/jbac_core)

---

## 1. APPLICATION OVERVIEW

This is an **Angular-based frontend** for the **Jesus Believers' Association of Christians (JBAC)** platform. The application provides a comprehensive Christian community management system with multiple features for believers, pastors, churches, organizations, and various ministries.

**Technology Stack:**
- Angular (version unclear from analysis)
- NgBootstrap for UI components
- TypeScript
- RxJS for reactive programming
- SweetAlert2 for notifications
- Angular Forms (Reactive & Template-driven)

---

## 2. COMPONENT STRUCTURE

### A. Core Application Components

| Component | Purpose | Type |
|-----------|---------|------|
| `AppComponent` | Root application component | App Root |
| `HeaderComponent` | Navigation header/menu | Shared |
| `FooterComponent` | Footer section | Shared |
| `HomeComponent` | Home/landing page | Home Module |

### B. Feature Components (Jesus Module)

#### **Authentication & User Management**
- `LoginComponent` - Password-based login with role selection (Believer, Pastor, Student, etc.)
- `SignupComponent` - User registration
- `ProfileComponent` - User profile management
- `BelieverRegisterComponent` - Believer profile registration
- `PastorRegisterComponent` - Pastor profile registration
- `StudentRegisterComponent` - Student profile registration
- `ChurchRegisterComponent` - Church profile registration
- `OrganizationRegisterComponent` - Organization/Company registration
- `MinistryRegisterComponent` - Ministry registration
- `PastorAssociationRegisterComponent` - Pastor's association registration

#### **Directory & Search**
- `ChurchPastorSearchComponent` - Search for pastors and churches
- `ChurchTimingsComponent` - Church service timings listing/search
- `GalleryComponent` - Photo gallery management
- `SubGalleryComponent` - Gallery subcategory/detail view

#### **Meetings & Events**
- `EventsComponent` - Events listing and search
- `AddMeetingsComponent` - Create/submit meeting details
- `MeetingComponent` - Meeting detail view
- `AttacksComponent` - Christian attack incidents/challenges
- `AddAttacksComponent` - Report Christian attacks

#### **Business & Jobs**
- `BusinessComponent` - Business directory/listings
- `AddBusinessComponent` - Add business profile
- `JobsComponent` - Job listings
- `AddJobsComponent` - Post new job listing

#### **Educational & Development**
- `InstituteComponent` - Educational institutes listing
- `AddInstituteComponent` - Add institute information
- `DownloadsComponent` - Resource downloads section
- `HelpComponent` - Help/support requests
- `WishComponent` - Wish/prayer request system
- `EntryComponent` - Entry/registration form
- `NamoduComponent` - Specific program (Telugu: "Namodu")

#### **Content & Information**
- `AboutComponent` - About JBAC/organization info
- `ServicesComponent` - Services offered
- `NewsComponent` - News management and listing
- `SubnewsComponent` - News detail/subcategory view
- `NewsPageComponent` - News page display
- `UpdateComponent` - Updates/announcements
- `VideosPageComponent` - Video content
- `SubVideoComponent` - Video detail view
- `ContactUsComponent` - Contact form
- `TermsComponent` - Terms & Conditions
- `PrivacyPolicyComponent` - Privacy policy

#### **Additional Components**
- `LeadersComponent` - Leadership/members directory
- `MarriagesComponent` - Marriage records/matching
- `AddMarriagesComponent` - Marriage information submission
- `CarouselComponent` - Image carousel
- `WebHelpComponent` - Web help/support
- `Ap1croreBelieversComponent` - State-specific believer campaign
- `ApChristianPoliticsComponent` - Christian politics discussion
- `ChristianAttackVideoComponent` - Attack incident videos
- `InjusticeComponent` - Social justice issues
- `WingsComponent` - Ministry wings/departments
- `WorkComponent` - Work/ministry opportunities
- `OurhelpComponent` - Our help/assistance programs
- `ChurchGoComponent` - Church navigation/directory
- `PaymentGatewayComponent` - Payment processing
- `TechsolComponent` - Technical solutions
- `CollegesComponent` - College information
- `JosephViewComponent` - Specific ministry view
- `SuppRegComponent` - Supporter registration
- `SurveyNewsComponent` - Survey-based news

---

## 3. SERVICE ARCHITECTURE

### Central Service: `ServiceService`

This is the main service handling all HTTP communication with the Django backend.

**Key Methods Found:**
- `getdenomation()` - Fetch denominations/church types
- `getdistrict()` - Fetch district list
- `getwing()` - Fetch ministry wings/departments
- `getpastorsfilters(data)` - Search/filter pastors with parameters
- `passwordlogin(data)` - Login with email/phone and password
- `passwordwebsitelogin` - API endpoint for password login
- `postattacks(data)` - Submit Christian attack/incident report
- `addNew(data)` - Generic method to add new records
- `updateNew(data)` - Generic method to update records
- `deleteNew(data)` - Generic method to delete records
- `getlgstatus(status)` - Get login/authentication status

**Base Configuration:**
- Uses `HttpClient` from Angular
- Has a `testApi` property that stores the base API URL
- Uses `BehaviorSubject` for state management

---

## 4. ROUTING STRUCTURE

### Main Application Routes

Based on `app-routing.module.ts`:

```
/                           → HomeComponent
/about                      → AboutComponent
/events                     → EventsComponent
/services                   → ServicesComponent
/gallery                    → GalleryComponent
/business                   → BusinessComponent
/church_timings             → ChurchTimingsComponent
/contactus                  → ContactusComponent
/techsol                    → TechsolComponent
/church-pastor-search       → ChurchPastorSearchComponent
/believerregister           → BelieverRegisterComponent
/pastorregister             → PastorRegisterComponent
/studentregister            → StudentRegisterComponent
/churchregister             → ChurchRegisterComponent
/organisationregister       → OrganisationRegisterComponent
/pastorassociationregister  → PastorAssociationRegisterComponent
/ministryregister           → MinistryRegisterComponent
[... additional routes for add/edit components and features]
```

---

## 5. DATA MODELS & INTERFACES EXPECTED

### User/Profile Models
```typescript
Believer {
  believer_id: number
  full_name: string
  gender: string
  whatsapp_number: string
  date_of_birth: date
  life_goal: string
  hobbies: string
  youtube_channel: string
  additional_information: string
  mobile_number: string
  email: string
}

Pastor {
  pastor_id: number
  pastor_name: string
  church_name: string
  district: string
  state: string
  mobile_number: string
  email: string
  year_joined: number
  denomination: string
}

Church {
  church_id: number
  church_name: string
  pastor_name: string
  pastor_id: number
  district: string
  state: string
  village: string
  mandal: string
  mobile_number: string
  email: string
  latitude: float
  longitude: float
}

Student {
  student_id: number
  full_name: string
  roll_number: string
  institution: string
  gender: string
  date_of_birth: date
  mobile_number: string
  email: string
  wing: string
}

Organization {
  org_id: number
  organization_name: string
  organization_type: string
  website: string
  service_name: string
  mobile_number: string
  email: string
  address: string
}
```

### Event/Meeting Models
```typescript
Meeting {
  meeting_id: number
  title: string
  description: string
  start_date: date
  end_date: date
  organizer_name: string
  estimated_attendance: number
  organizer_phone: string
  address: string
  district: string
  state: string
  city_area: string
  mandal: string
  village: string
  meeting_type: string
  denomination: string
  ministry: string
  latitude: float
  longitude: float
  google_map_location: string
  poster: file/image
  youtube_link: string
  additional_info: string
}

Event {
  event_id: number
  title: string
  date: date
  description: string
  location: string
}
```

### Content Models
```typescript
News {
  news_id: number
  title: string
  content: string
  summary: string
  category: string
  newspaper: string
  image: file
  published_date: date
}

NewsCategory {
  id: number
  name: string  // e.g., "christian-media", "honorarium", "jobs", "health"
}

Update {
  update_id: number
  title: string
  content: string
  category: string
  image: file
  published_date: date
}
```

### Directory/Lookup Models
```typescript
District {
  district_id: number
  name: string
  state: string
}

Denomination {
  denomination_id: number
  name: string
  description: string
}

Wing/Ministry {
  wing_id: number
  name: string
  description: string
}
```

---

## 6. FORMS AND USER INPUTS

### Authentication Forms
```
LoginForm {
  role: select (Believer|Pastor|Student|Church|Organization|Ministry|PastorAssociation)
  identifier: string (phone or email)
  password: string
}

OTPRequestForm {
  role: select
  identifier: string
}

OTPVerifyForm {
  otp: string (6 digits)
}
```

### Registration Forms
```
BelieverRegistrationForm {
  full_name: string
  gender: select
  mobile_number: string (required, unique)
  email: string (optional)
  password: string
  whatsapp_number: string
  date_of_birth: date
  life_goal: text
  hobbies: text
  youtube_channel: string
  additional_information: text
  consent: checkbox (privacy acknowledgment)
}

PastorRegistrationForm {
  pastor_name: string
  church_name: string
  mobile_number: string
  email: string
  password: string
  district: select
  state: select
  denomination: select
  years_in_ministry: number
  additional_info: text
  consent: checkbox
}

ChurchRegistrationForm {
  church_name: string
  pastor_name: string
  pastor_id: string
  mobile_number: string
  email: string
  password: string
  district: select
  village: string
  mandal: string
  denomination: select
  service_name: string
  website: string
  consent: checkbox
}

StudentRegistrationForm {
  full_name: string
  mobile_number: string
  email: string
  password: string
  institution: string
  roll_number: string
  date_of_birth: date
  gender: select
  wing: select (ministry wing)
  consent: checkbox
}

OrganizationRegistrationForm {
  organization_name: string
  organization_type: select
  mobile_number: string
  email: string
  password: string
  website: string
  service_name: string
  consent: checkbox
}

MinistryRegistrationForm {
  ministry_name: string
  ministry_type: string
  leader_name: string
  mobile_number: string
  email: string
  password: string
  focus_area: string
  consent: checkbox
}
```

### Content Submission Forms
```
MeetingSubmissionForm {
  title: string (required)
  description: text (required)
  start_date: date (required)
  end_date: date (required)
  organizer_name: string (required)
  estimated_attendance: number (required)
  organizer_phone: string (required, not shown to public)
  address: text (required)
  district: select (required)
  state: string (required)
  city_area: string
  mandal: string
  village: string
  meeting_type: select (optional)
  denomination: select (optional)
  ministry: select (optional)
  latitude: number (auto-filled)
  longitude: number (auto-filled)
  google_map_location: url (optional)
  poster: file (image)
  youtube_link: url (optional)
  additional_info: text
}

NewsSubmissionForm {
  title: string (required)
  content: text (required)
  category: select (required)
  summary: text
  newspaper: select (optional)
  image: file (optional)
}

EventsSearchForm {
  meeting_type: select
  denomination: select
  ministry: select
  date: date
  district: select
  city_area: string
  mandal: string
  village: string
}

BusinessSearchForm {
  district: select
  city: string
  business_type: select
}

JobsSearchForm {
  district: select
  job_type: select
  experience_level: select
}

PastorSearchForm {
  name: string
  district: select
  state: select
  denomination: select
}
```

### User Input Fields Summary
- **Selects:** role, district, state, gender, denomination, ministry, category, meeting_type, wing
- **Text Inputs:** names, phone numbers, emails, URLs, descriptions
- **Dates:** birth dates, event dates, meeting dates
- **Coordinates:** latitude, longitude (auto-filled from geolocation)
- **Files:** images, posters, documents
- **Textareas:** descriptions, goals, hobbies, additional information
- **Checkboxes:** consent/privacy acknowledgment

---

## 7. API ENDPOINTS REQUIRED FROM DJANGO BACKEND

### Authentication Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST | `/api/auth/login/` | Password login | `{role, identifier, password}` | `{token, user_data, role}` |
| POST | `/api/auth/otp-request/` | Request OTP | `{role, identifier}` | `{status, message}` |
| POST | `/api/auth/otp-verify/` | Verify OTP | `{otp, challenge_id}` | `{token, user_data}` |
| POST | `/api/auth/logout/` | Logout | `{}` | `{status}` |
| GET | `/api/auth/status/` | Get login status | - | `{is_authenticated, user_id, role}` |

### User Registration Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST | `/api/believers/register/` | Register believer | `BelieverProfile data` | `{user_id, believer_id, token}` |
| POST | `/api/pastors/register/` | Register pastor | `PastorProfile data` | `{user_id, pastor_id, token}` |
| POST | `/api/students/register/` | Register student | `StudentProfile data` | `{user_id, student_id, token}` |
| POST | `/api/churches/register/` | Register church | `ChurchProfile data` | `{user_id, church_id, token}` |
| POST | `/api/organizations/register/` | Register organization | `OrganizationProfile data` | `{user_id, org_id, token}` |
| POST | `/api/ministries/register/` | Register ministry | `MinistryProfile data` | `{user_id, ministry_id, token}` |
| POST | `/api/pastor-associations/register/` | Register pastor association | `PastorAssociation data` | `{user_id, assoc_id, token}` |

### User Profile Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| GET | `/api/profile/` | Get current user profile | - | `{user_id, role, profile_data}` |
| PUT | `/api/profile/update/` | Update profile | `{profile_fields}` | `{updated_profile}` |
| GET | `/api/profile/<type>/<id>/` | Get specific profile | - | `{profile_data}` |
| DELETE | `/api/profile/delete/` | Delete profile | - | `{status}` |

### Directory & Search Endpoints

| Method | Endpoint | Purpose | Query Parameters | Response |
|--------|----------|---------|-------------------|----------|
| GET | `/api/pastors/search/` | Search pastors | `name, district, state, denomination` | `{count, results: [pastors]}` |
| GET | `/api/churches/search/` | Search churches | `name, district, state` | `{count, results: [churches]}` |
| GET | `/api/directory/public-pastors/` | Public pastor directory | `district, state` | `{results: [approved_pastors]}` |
| GET | `/api/directory/public-churches/` | Public church directory | `district, state` | `{results: [approved_churches]}` |
| GET | `/api/directory/map-search/` | Map-based search | `district, state, lat, lng, radius` | `{markers: [{lat, lng, name, pastor, district}]}` |

### Meetings/Events Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST | `/api/meetings/submit/` | Submit meeting (requires auth) | `MeetingSubmission data` | `{meeting_id, status, message}` |
| GET | `/api/meetings/` | List meetings | `filters: type, denomination, ministry, date, district` | `{count, results: [meetings]}` |
| GET | `/api/meetings/<id>/` | Get meeting details | - | `{meeting_data, organizer_contact}` |
| PUT | `/api/meetings/<id>/update/` | Update meeting (auth required) | `{updated_fields}` | `{updated_meeting}` |
| DELETE | `/api/meetings/<id>/delete/` | Delete meeting (auth required) | - | `{status}` |

### News/Updates Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST | `/api/news/submit/` | Submit news article (auth required) | `NewsArticle data` | `{article_id, status}` |
| GET | `/api/news/` | List news articles | `category, newspaper, search_query, page` | `{count, results: [news]}` |
| GET | `/api/news/<id>/` | Get news detail | - | `{news_data}` |
| GET | `/api/news/categories/` | Get news categories | - | `{categories: [{id, name, description}]}` |
| PUT | `/api/news/<id>/update/` | Update news (auth required) | `{updated_fields}` | `{updated_news}` |
| DELETE | `/api/news/<id>/delete/` | Delete news (auth required) | - | `{status}` |

### Business & Jobs Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST | `/api/businesses/add/` | Add business (auth required) | `Business data` | `{business_id, status}` |
| GET | `/api/businesses/` | List businesses | `district, city, business_type, search` | `{count, results: [businesses]}` |
| GET | `/api/businesses/<id>/` | Get business detail | - | `{business_data}` |
| POST | `/api/jobs/add/` | Post job (auth required) | `Job data` | `{job_id, status}` |
| GET | `/api/jobs/` | List jobs | `district, job_type, search` | `{count, results: [jobs]}` |
| GET | `/api/jobs/<id>/` | Get job detail | - | `{job_data}` |

### Educational Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST | `/api/institutes/add/` | Add institute (auth required) | `Institute data` | `{institute_id, status}` |
| GET | `/api/institutes/` | List institutes | `district, state, institute_type` | `{count, results: [institutes]}` |
| GET | `/api/institutes/<id>/` | Get institute detail | - | `{institute_data}` |

### Incidents/Attacks Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST | `/api/incidents/report/` | Report Christian attack (auth required) | `{title, description, location, date, witnesses}` | `{incident_id, status}` |
| GET | `/api/incidents/` | List incidents | `district, date_range, severity` | `{count, results: [incidents]}` |
| GET | `/api/incidents/<id>/` | Get incident detail | - | `{incident_data}` |

### Lookup/Reference Data Endpoints

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| GET | `/api/lookups/districts/` | Get all districts | `{districts: [{id, name, state}]}` |
| GET | `/api/lookups/states/` | Get all states | `{states: [{id, name, code}]}` |
| GET | `/api/lookups/denominations/` | Get denominations | `{denominations: [{id, name}]}` |
| GET | `/api/lookups/wings/` | Get ministry wings | `{wings: [{id, name, description}]}` |
| GET | `/api/lookups/meeting-types/` | Get meeting types | `{types: [{id, name}]}` |
| GET | `/api/lookups/business-types/` | Get business types | `{types: [{id, name}]}` |
| GET | `/api/lookups/job-categories/` | Get job categories | `{categories: [{id, name}]}` |
| GET | `/api/lookups/news-categories/` | Get news categories | `{categories: [{id, name}]}` |

### Prayer/Wish Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| POST | `/api/prayers/submit/` | Submit prayer request (auth required) | `{title, description, category}` | `{prayer_id, status}` |
| GET | `/api/prayers/` | List prayers | `category, created_by` | `{count, results: [prayers]}` |
| GET | `/api/prayers/<id>/` | Get prayer detail | - | `{prayer_data}` |

### Leaders/Marriages Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| GET | `/api/leaders/` | Get leaders directory | `district, state, role` | `{count, results: [leaders]}` |
| GET | `/api/marriages/` | List marriages/matchings | `age_range, district` | `{count, results: [matches]}` |
| POST | `/api/marriages/add/` | Add marriage profile (auth required) | `Marriage data` | `{marriage_id, status}` |

### Gallery/Media Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| GET | `/api/gallery/` | List gallery categories | - | `{categories: [{id, name, image_count}]}` |
| GET | `/api/gallery/<category_id>/` | Get gallery images | `page, per_page` | `{count, results: [images]}` |
| POST | `/api/gallery/upload/` | Upload gallery image (auth required) | `{image_file, category_id, title}` | `{image_id, url}` |

### Content Endpoints

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| GET | `/api/about-us/` | Get About Us content | `{sections: [content]}` |
| GET | `/api/services/` | Get Services content | `{services: [{id, name, description}]}` |
| GET | `/api/terms/` | Get Terms & Conditions | `{content}` |
| GET | `/api/privacy-policy/` | Get Privacy Policy | `{content}` |
| GET | `/api/contact/` | Get contact information | `{email, phone, address}` |

### Download/Resources Endpoints

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| GET | `/api/resources/` | List downloadable resources | `{count, results: [resources]}` |
| GET | `/api/resources/<id>/download/` | Download resource | File stream |

---

## 8. NAVIGATION STRUCTURE

### Main Menu Items
```
Home (/)
├── About Us (/about)
├── Services (/services)
├── Events (/events)
├── Gallery (/gallery)
├── Directory Search (/directory/search)
├── Church Timings (/church_timings)
├── News & Updates (/news)
├── Contact Us (/contactus)
├── Terms & Conditions (/terms)
├── Privacy Policy (/privacy-policy)
└── Help & Support (/help)

Registration Center
├── Believer Register (/believerregister)
├── Pastor Register (/pastorregister)
├── Student Register (/studentregister)
├── Church Register (/churchregister)
├── Organization Register (/organisationregister)
├── Ministry Register (/ministryregister)
└── Pastor Association Register (/pastorassociationregister)

User Dashboard (Auth Required)
├── My Profile (/profile)
├── My Meetings (/my-meetings)
├── My Submissions (/my-submissions)
└── Settings (/settings)

Admin Functions (Auth Required - Admin Role)
├── Approve Submissions (/admin/approvals)
├── Manage Users (/admin/users)
├── Content Management (/admin/content)
└── Analytics (/admin/analytics)

Features
├── Church Search (/church-pastor-search)
├── Business Directory (/business)
├── Jobs Board (/jobs)
├── Educational Institutes (/institute)
├── Prayer Requests (/wish)
├── Event Calendar (/events)
├── Marriage Matching (/marriages)
├── Christian Incidents (/attacks)
└── Downloads (/downloads)
```

---

## 9. AUTHENTICATION & SECURITY REQUIREMENTS

### Authentication Flow
1. User selects **role** (Believer, Pastor, Student, etc.)
2. User enters **identifier** (mobile number or email)
3. User can choose:
   - **Password Login** → `/api/auth/login/`
   - **OTP Login** → `/api/auth/otp-request/` → `/api/auth/otp-verify/`

4. Backend returns **authentication token** (JWT or session)
5. Frontend stores token and uses it for subsequent requests
6. Components check authentication status via `getlgstatus()` or similar

### Authorization Requirements
- Public Routes: Home, About, Services, Gallery, Directory Search, News, Terms, Privacy
- Auth Required: Profile management, meeting submission, news submission, prayer requests, user dashboard
- Admin Required: Content approvals, user management, analytics

### Session Management
- Tokens stored in `sessionStorage` and `localStorage`
- `sessionStorage.getItem('category')` - stores user category/role
- `localStorage.setItem('key_id')` - stores user ID

---

## 10. EXPECTED RESPONSE FORMATS

### Standard Success Response
```json
{
  "status": 200 or 201,
  "message": "Success message",
  "data": {}
}
```

### Standard Error Response
```json
{
  "status": 400 or 500,
  "message": "Error message",
  "errors": {}
}
```

### List Response
```json
{
  "status": 200,
  "count": 45,
  "next": "/api/endpoint/?page=2",
  "previous": null,
  "data": [{}]
}
```

### Paginated Response
```json
{
  "status": 200,
  "count": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5,
  "results": [{}]
}
```

---

## 11. KEY FEATURES & WORKFLOW

### User Registration Workflow
1. User selects registration path (believer/pastor/student/etc.)
2. Fills out profile-specific form
3. Frontend validates data
4. POST to `/api/<role>/register/`
5. Backend creates User and Profile
6. Returns user_id, role, and auth token
7. Frontend stores token and redirects to dashboard

### Meeting Submission Workflow
1. User fills MeetingSubmissionForm
2. Can optionally auto-fill coordinates via geolocation
3. POST to `/api/meetings/submit/`
4. Backend stores meeting with `is_published=False`
5. Admin reviews and approves
6. Approved meetings appear in `/api/meetings/`

### Search & Discovery Workflow
1. User selects filters (district, denomination, type, etc.)
2. Frontend calls `/api/<resource>/search/` with parameters
3. Backend filters and returns results
4. Results displayed in cards/list view
5. User can click for detailed view

### Event/Meeting Calendar
1. Frontend fetches meetings via `/api/meetings/`
2. Groups by date/location
3. Displays on calendar or list view
4. Clicking event shows details and organizer info
5. "Get Directions" link uses Google Maps

---

## 12. NOTABLE IMPLEMENTATION PATTERNS

### State Management
- Uses `BehaviorSubject` in service layer
- Components subscribe to observables
- Local component state for UI

### Form Handling
- Reactive Forms with `FormBuilder` and `FormGroup`
- Custom validators for phone/email uniqueness
- Password confirmation matching

### HTTP Client Configuration
- Centralized in `ServiceService`
- Base API URL configurable
- Error handling with SweetAlert2 notifications

### UI Patterns
- Modal dialogs via `NgbModal`
- Alerts via SweetAlert2
- Pagination for large lists
- Search/filter forms above results
- Card-based layout for listings

### Data Display
- Tables with sorting/filtering
- Dropdown cascades (State → District → Mandal → Village)
- Image galleries with thumbnails
- Map views for location-based data
- Timestamps for created/updated dates

---

## SUMMARY TABLE: ALL API ENDPOINTS

### Quick Reference by Category

**Authentication (5 endpoints)**
- `POST /api/auth/login/`
- `POST /api/auth/otp-request/`
- `POST /api/auth/otp-verify/`
- `POST /api/auth/logout/`
- `GET /api/auth/status/`

**Registrations (7 endpoints)**
- `POST /api/believers/register/`
- `POST /api/pastors/register/`
- `POST /api/students/register/`
- `POST /api/churches/register/`
- `POST /api/organizations/register/`
- `POST /api/ministries/register/`
- `POST /api/pastor-associations/register/`

**Profile Management (4 endpoints)**
- `GET /api/profile/`
- `PUT /api/profile/update/`
- `GET /api/profile/<type>/<id>/`
- `DELETE /api/profile/delete/`

**Directory & Search (4 endpoints)**
- `GET /api/pastors/search/`
- `GET /api/churches/search/`
- `GET /api/directory/public-pastors/`
- `GET /api/directory/public-churches/`
- `GET /api/directory/map-search/`

**Meetings (5 endpoints)**
- `POST /api/meetings/submit/`
- `GET /api/meetings/`
- `GET /api/meetings/<id>/`
- `PUT /api/meetings/<id>/update/`
- `DELETE /api/meetings/<id>/delete/`

**News (5 endpoints)**
- `POST /api/news/submit/`
- `GET /api/news/`
- `GET /api/news/<id>/`
- `GET /api/news/categories/`
- `PUT/DELETE` variants

**Business & Jobs (6 endpoints)**
- `POST /api/businesses/add/`
- `GET /api/businesses/[?params]`
- `GET /api/businesses/<id>/`
- `POST /api/jobs/add/`
- `GET /api/jobs/[?params]`
- `GET /api/jobs/<id>/`

**Lookup Data (8 endpoints)**
- `GET /api/lookups/districts/`
- `GET /api/lookups/states/`
- `GET /api/lookups/denominations/`
- `GET /api/lookups/wings/`
- `GET /api/lookups/meeting-types/`
- `GET /api/lookups/business-types/`
- `GET /api/lookups/job-categories/`
- `GET /api/lookups/news-categories/`

**Additional (12+ endpoints)**
- Institutes, Incidents/Attacks, Prayers, Leaders, Marriages, Gallery, Content, Downloads

**Total Expected Endpoints: ~70+**

---

**Document Generated:** May 18, 2026
**Analysis Scope:** Angular Frontend (r-karra/jbac_core GitHub Repository)
**Status:** Complete - Ready for Backend Implementation
