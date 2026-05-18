from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View

from directory.models import (
	BelieverProfile,
	ChurchProfile,
	OrganizationProfile,
	PastorProfile,
	StudentProfile,
	get_profile_for_user,
)
from updates.models import NewsArticle
from .models import AboutPageContent, NavigationGroup
from .submission_forms import (
	JobSubmissionForm,
	BusinessSubmissionForm,
	InstituteSubmissionForm,
	IncidentReportForm,
	PrayerSubmissionForm,
)
from .account_forms import (
	ChurchTimingsForm,
	MeetingsForm,
	JobsForm,
	BusinessForm,
	InstituteForm,
	AttacksForm,
	AdsForm,
	LeadersForm,
	# Search forms
	InstitutesSearchForm,
	MarriagesSearchForm,
	JobsSearchForm,
	HelpSearchForm,
	NewsSearchForm,
	BusinessSearchForm,
	WingsSearchForm,
	OrganizationSearchForm,
)


ABOUT_SECTIONS = {
	"about-us": {
		"title_te": "మా గురించి",
		"title_en": "About Us",
		"description": "JBAC is a Christian community platform focused on registrations, directory services, and trusted communication.",
		"youtube_embed_src": "",
		"points": [
			"Secure registrations for believers, pastors, students, churches, and organizations.",
			"Bilingual support in Telugu and English.",
			"Admin-reviewed visibility for public ministry records.",
		],
	},
	"our-help": {
		"title_te": "మీకు మా సహాయం",
		"title_en": "Our Help",
		"description": "We help churches and believers onboard quickly and use JBAC services effectively.",
		"youtube_embed_src": "",
		"points": [
			"Registration support for all role categories.",
			"Directory discoverability for approved ministries.",
			"Community updates and communication channels.",
		],
	},
	"how-to-use": {
		"title_te": "వెబ్ సైట్ ఎలా ఉపయోగించాలి",
		"title_en": "How to Use the Website",
		"description": "Follow these steps to use the website productively.",
		"youtube_embed_src": "",
		"points": [
			"Choose the correct registration type.",
			"Login with password or OTP.",
			"Use search and district map features after admin approvals.",
		],
	},
	"pastor-guidance-articles": {
		"title_te": "చర్చి పాస్టర్ గైడెన్స్ ఆర్టికల్",
		"title_en": "Church Pastor Guidance Articles",
		"description": "Guidance topics for pastors and church leaders.",
		"youtube_embed_src": "",
		"points": [
			"Digital presence for local church outreach.",
			"Member care and confidentiality practices.",
			"Using announcements and prayer support responsibly.",
		],
	},
	"add-your-church": {
		"title_te": "మీ చర్చి మా వెబ్‌సైట్‌లో ఎలా చేర్చాలి",
		"title_en": "How to Add Your Church to the Website",
		"description": "Register a church profile and include location details for map visibility.",
		"youtube_embed_src": "",
		"points": [
			"Use Church Registration under Register menu.",
			"Fill church name, pastor name, district, and contact details.",
			"Add latitude and longitude to appear in district map search.",
		],
	},
	"add-announcements": {
		"title_te": "క్రైస్తవులకు సంబంధించిన మాటలు చేర్చండి",
		"title_en": "Add Christian Announcements",
		"description": "Share verified Christian community announcements through JBAC admin moderation.",
		"youtube_embed_src": "",
		"points": [
			"Prepare title, summary, and event details.",
			"Contact JBAC admins for publishing workflow.",
			"Published announcements appear in the News section.",
		],
	},
	"prayer-requests": {
		"title_te": "క్రైస్తవుల కోసం ప్రార్థన అవసరాలు",
		"title_en": "Prayer Requests for Christians",
		"description": "You can share prayer requests with council support channels.",
		"youtube_embed_src": "",
		"points": [
			"Include person name and short prayer context.",
			"Avoid sensitive private information.",
			"Reach out via contact page for urgent cases.",
		],
	},
	"photo-gallery": {
		"title_te": "ఫోటో గ్యాలరీ",
		"title_en": "Photo Gallery",
		"description": "A curated gallery area for Christian events and ministry moments.",
		"youtube_embed_src": "",
		"points": [
			"Event photos can be shared after moderation.",
			"Use high-quality images with proper captions.",
			"Community-safe content only.",
		],
	},
}


ABOUT_MENU = [
	("about-us", "మా గురించి", "About Us"),
	("our-help", "మీకు మా సహాయం", "Our Help"),
	("how-to-use", "వెబ్ సైట్ ఎలా ఉపయోగించాలి", "How to Use the Website"),
	("pastor-guidance-articles", "చర్చి పాస్టర్ గైడెన్స్ ఆర్టికల్", "Church Pastor Guidance Articles"),
	("add-your-church", "మీ చర్చి మా వెబ్‌సైట్‌లో ఎలా చేర్చాలి", "How to Add Your Church to the Website"),
	("add-announcements", "క్రైస్తవులకు సంబంధించిన మాటలు చేర్చండి", "Add Christian Announcements"),
	("prayer-requests", "క్రైస్తవుల కోసం ప్రార్థన అవసరాలు", "Prayer Requests for Christians"),
	("photo-gallery", "ఫోటో గ్యాలరీ", "Photo Gallery"),
]



def home(request):
	stats = {
		"believers": BelieverProfile.objects.count(),
		"pastors": PastorProfile.objects.count(),
		"students": StudentProfile.objects.count(),
		"churches": ChurchProfile.objects.count(),
		"organizations": OrganizationProfile.objects.count(),
	}
	featured_articles = NewsArticle.objects.filter(is_published=True, is_featured=True)[:3]
	latest_articles = NewsArticle.objects.filter(is_published=True)[:4]
	return render(
		request,
		"core/home.html",
		{
			"stats": stats,
			"featured_articles": featured_articles,
			"latest_articles": latest_articles,
		},
	)


def about(request):
	return render(request, "core/about.html")


def about_subpage(request, section=None):
	content_rows = list(AboutPageContent.objects.filter(is_active=True))
	menu_items = []
	section_map = {}

	if content_rows:
		for row in content_rows:
			section_map[row.section_slug] = {
				"title_te": row.page_title_te,
				"title_en": row.page_title_en,
				"description": row.description,
				"youtube_embed_src": row.youtube_embed_src(),
				"image": row.image,
				"pdf": row.pdf,
				"points": row.points(),
			}
			menu_items.append(
				{
					"slug": row.section_slug,
					"title_te": row.menu_title_te,
					"title_en": row.menu_title_en,
					"active": row.section_slug == section,
				}
			)
	else:
		section_map = ABOUT_SECTIONS
		for slug, te, en in ABOUT_MENU:
			menu_items.append(
				{
					"slug": slug,
					"title_te": te,
					"title_en": en,
					"active": slug == section,
				}
			)

	section_data = section_map.get(section) if section else None
	if section and section_data is None:
		section = None

	return render(
		request,
		"core/about_subpage.html",
		{
			"section": section,
			"section_data": section_data,
			"menu_items": menu_items,
			"content_source": "admin" if content_rows else "default",
			"has_selected_content": section_data is not None,
		},
	)


def navigation_group_page(request, slug):
	group = get_object_or_404(
		NavigationGroup.objects.prefetch_related("items"),
		slug=slug,
		is_active=True,
	)
	
	# Check if user is authenticated
	if not request.user.is_authenticated:
		# Show login message for protected groups (Services, Account)
		show_prompt = True
		nav_items = []
		context = {
			"nav_group": group,
			"nav_items": nav_items,
			"show_prompt": show_prompt,
			"login_message": "Dear user, please login to use more services.",
		}
		return render(request, "core/navigation_group.html", context)
	
	# User is authenticated - show available items
	items = group.items.filter(is_active=True)
	
	# Filter out staff-only items if user is not staff
	if not request.user.is_staff:
		items = items.filter(staff_only=False)
	
	return render(
		request,
		"core/navigation_group.html",
		{
			"nav_group": group,
			"nav_items": items,
			"show_prompt": False,
		},
	)


def contact(request):
	return render(request, "core/contact.html")


def privacy_policy(request):
	return render(request, "core/privacy_policy.html")


def terms_conditions(request):
	return render(request, "core/terms_conditions.html")


@login_required
def dashboard(request):
	profile = get_profile_for_user(request.user)
	return render(request, "core/dashboard.html", {"profile": profile})


@staff_member_required
def admin_dashboard(request):
	stats = {
		"users": request.user.__class__.objects.count(),
		"pending_believers": BelieverProfile.objects.filter(is_approved=False).count(),
		"pending_pastors": PastorProfile.objects.filter(is_approved=False).count(),
		"pending_students": StudentProfile.objects.filter(is_approved=False).count(),
		"pending_churches": ChurchProfile.objects.filter(is_approved=False).count(),
		"pending_organizations": OrganizationProfile.objects.filter(is_approved=False).count(),
	}
	recent_registrations = {
		"believers": BelieverProfile.objects.select_related("user").order_by("-created_at")[:5],
		"pastors": PastorProfile.objects.select_related("user").order_by("-created_at")[:5],
		"churches": ChurchProfile.objects.select_related("user").order_by("-created_at")[:5],
	}
	return render(
		request,
		"core/admin_dashboard.html",
		{"stats": stats, "recent_registrations": recent_registrations},
	)


# ============================================================================
# SERVICE SUBMISSION VIEWS
# ============================================================================

@login_required
def job_submission(request):
	if request.method == "POST":
		form = JobSubmissionForm(request.POST)
		if form.is_valid():
			job = form.save(commit=False)
			job.posted_by = request.user
			job.save()
			messages.success(request, "Job listing submitted successfully! It will be visible after admin approval.")
			return redirect("core:dashboard")
	else:
		form = JobSubmissionForm()
	return render(request, "core/job_submission.html", {"form": form})


@login_required
def business_submission(request):
	if request.method == "POST":
		form = BusinessSubmissionForm(request.POST)
		if form.is_valid():
			business = form.save(commit=False)
			business.posted_by = request.user
			business.save()
			messages.success(request, "Business listing submitted successfully! It will be visible after admin approval.")
			return redirect("core:dashboard")
	else:
		form = BusinessSubmissionForm()
	return render(request, "core/business_submission.html", {"form": form})


@login_required
def institute_submission(request):
	if request.method == "POST":
		form = InstituteSubmissionForm(request.POST)
		if form.is_valid():
			institute = form.save(commit=False)
			institute.posted_by = request.user
			institute.save()
			messages.success(request, "Institute information submitted successfully! It will be visible after admin approval.")
			return redirect("core:dashboard")
	else:
		form = InstituteSubmissionForm()
	return render(request, "core/institute_submission.html", {"form": form})


@login_required
def incident_report(request):
	if request.method == "POST":
		form = IncidentReportForm(request.POST)
		if form.is_valid():
			incident = form.save(commit=False)
			incident.reported_by = request.user
			incident.save()
			messages.success(request, "Incident report submitted successfully! Our team will review it.")
			return redirect("core:dashboard")
	else:
		form = IncidentReportForm()
	return render(request, "core/incident_report.html", {"form": form})


@login_required
def prayer_submission(request):
	if request.method == "POST":
		form = PrayerSubmissionForm(request.POST)
		if form.is_valid():
			prayer = form.save(commit=False)
			prayer.submitted_by = request.user
			prayer.save()
			messages.success(request, "Prayer request submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = PrayerSubmissionForm()
	return render(request, "core/prayer_submission.html", {"form": form})


# ============================================================================
# ACCOUNT SUBMISSION VIEWS
# ============================================================================

@login_required
def church_timings_submit(request):
	if request.method == "POST":
		form = ChurchTimingsForm(request.POST)
		if form.is_valid():
			# For now, save directly or create a model if needed
			messages.success(request, "Church timings submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = ChurchTimingsForm()
	return render(request, "core/church_timings_submit.html", {"form": form})


@login_required
def meetings_submit(request):
	if request.method == "POST":
		form = MeetingsForm(request.POST)
		if form.is_valid():
			meeting = form.save(commit=False)
			meeting.created_by = request.user
			meeting.save()
			messages.success(request, "Meeting submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = MeetingsForm()
	return render(request, "core/meetings_submit.html", {"form": form})


@login_required
def jobs_submit(request):
	if request.method == "POST":
		form = JobsForm(request.POST)
		if form.is_valid():
			job = form.save(commit=False)
			job.posted_by = request.user
			job.save()
			messages.success(request, "Job listing submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = JobsForm()
	return render(request, "core/jobs_submit.html", {"form": form})


@login_required
def business_submit(request):
	if request.method == "POST":
		form = BusinessForm(request.POST)
		if form.is_valid():
			business = form.save(commit=False)
			business.posted_by = request.user
			business.save()
			messages.success(request, "Business submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = BusinessForm()
	return render(request, "core/business_submit.html", {"form": form})


@login_required
def institute_submit(request):
	if request.method == "POST":
		form = InstituteForm(request.POST)
		if form.is_valid():
			institute = form.save(commit=False)
			institute.posted_by = request.user
			institute.save()
			messages.success(request, "Institute submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = InstituteForm()
	return render(request, "core/institute_submit.html", {"form": form})


@login_required
def attacks_submit(request):
	if request.method == "POST":
		form = AttacksForm(request.POST)
		if form.is_valid():
			attack = form.save(commit=False)
			attack.reported_by = request.user
			attack.save()
			messages.success(request, "Attack report submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = AttacksForm()
	return render(request, "core/attacks_submit.html", {"form": form})


@login_required
def ads_submit(request):
	if request.method == "POST":
		form = AdsForm(request.POST)
		if form.is_valid():
			messages.success(request, "Advertisement submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = AdsForm()
	return render(request, "core/ads_submit.html", {"form": form})


@login_required
def leaders_submit(request):
	if request.method == "POST":
		form = LeadersForm(request.POST)
		if form.is_valid():
			messages.success(request, "Leader information submitted successfully!")
			return redirect("core:dashboard")
	else:
		form = LeadersForm()
	return render(request, "core/leaders_submit.html", {"form": form})


# ============================================================================
# SERVICE SEARCH VIEWS
# ============================================================================

def institutes_search(request):
	form = InstitutesSearchForm(request.GET or None)
	results = []
	if form.is_valid() and request.GET:
		queryset = form.search()
		results = queryset
	return render(request, "core/institutes_search.html", {"form": form, "results": results})


def marriages_search(request):
	form = MarriagesSearchForm(request.GET or None)
	results = []
	if form.is_valid() and request.GET:
		queryset = form.search()
		results = queryset
	return render(request, "core/marriages_search.html", {"form": form, "results": results})


def jobs_search(request):
	form = JobsSearchForm(request.GET or None)
	results = []
	if form.is_valid() and request.GET:
		queryset = form.search()
		results = queryset
	return render(request, "core/jobs_search.html", {"form": form, "results": results})


def help_search(request):
	form = HelpSearchForm(request.GET or None)
	results = []
	if form.is_valid() and request.GET:
		queryset = form.search()
		results = queryset
	return render(request, "core/help_search.html", {"form": form, "results": results})


def business_search(request):
	form = BusinessSearchForm(request.GET or None)
	results = []
	if form.is_valid() and request.GET:
		queryset = form.search()
		results = queryset
	return render(request, "core/business_search.html", {"form": form, "results": results})


def wings_search(request):
	form = WingsSearchForm(request.GET or None)
	results = []
	if form.is_valid() and request.GET:
		queryset = form.search()
		results = queryset
	return render(request, "core/wings_search.html", {"form": form, "results": results})


def organization_search(request):
	form = OrganizationSearchForm(request.GET or None)
	results = []
	if form.is_valid() and request.GET:
		queryset = form.search()
		results = queryset
	return render(request, "core/organization_search.html", {"form": form, "results": results})
