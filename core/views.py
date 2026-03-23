from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from directory.models import (
	BelieverProfile,
	ChurchProfile,
	OrganizationProfile,
	PastorProfile,
	StudentProfile,
	get_profile_for_user,
)
from updates.models import NewsArticle
from .models import AboutPageContent


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
