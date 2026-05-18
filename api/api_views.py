from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

from directory.models import (
	BelieverProfile, ChurchProfile, OrganizationProfile, PastorProfile, 
	StudentProfile, Leader, Marriage, DISTRICT_CHOICES, STATE_CHOICES
)
from updates.models import NewsArticle
from meetings.models import Meeting, MEETING_TYPE_CHOICES, DENOMINATION_CHOICES
from jobs.models import Job, JobCategory, JOB_TYPE_CHOICES, EXPERIENCE_LEVEL_CHOICES
from businesses.models import Business, BusinessCategory, BUSINESS_TYPE_CHOICES
from institutes.models import Institute, InstituteCategory, INSTITUTE_TYPE_CHOICES
from incidents.models import Incident, INCIDENT_TYPE_CHOICES, SEVERITY_CHOICES, STATUS_CHOICES
from core.models import Prayer, GalleryCategory, GalleryImage, PRAYER_CATEGORY_CHOICES


# ============================================================================
# STATISTICS & PLATFORM DATA
# ============================================================================

@require_GET
def platform_stats_api(request):
	data = {
		"believers": BelieverProfile.objects.count(),
		"pastors": PastorProfile.objects.count(),
		"students": StudentProfile.objects.count(),
		"churches": ChurchProfile.objects.count(),
		"organizations": OrganizationProfile.objects.count(),
		"meetings": Meeting.objects.count(),
		"jobs": Job.objects.count(),
		"businesses": Business.objects.count(),
		"institutes": Institute.objects.count(),
		"incidents": Incident.objects.count(),
		"news_articles": NewsArticle.objects.count(),
	}
	return JsonResponse({"status": "ok", "data": data})


# ============================================================================
# DIRECTORY & SEARCH - PASTORS & CHURCHES
# ============================================================================

@require_GET
def pastors_api(request):
	query = request.GET.get("q", "").strip()
	district = request.GET.get("district", "").strip()
	state = request.GET.get("state", "").strip()

	items = PastorProfile.objects.filter(is_approved=True, is_public=True).select_related("user")
	if query:
		items = items.filter(
			Q(pastor_name__icontains=query)
			| Q(church_name__icontains=query)
			| Q(user__mobile_number__icontains=query)
		)
	if district:
		items = items.filter(district=district)
	if state:
		items = items.filter(state=state)

	data = [
		{
			"id": row.id,
			"pastor_name": row.pastor_name,
			"church_name": row.church_name,
			"district": row.district,
			"state": row.state,
			"latitude": float(row.latitude) if row.latitude else None,
			"longitude": float(row.longitude) if row.longitude else None,
			"mobile": row.user.mobile_number,
			"email": row.user.email,
			"years_of_ministry": row.years_of_ministry,
		}
		for row in items[:100]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


@require_GET
def churches_api(request):
	query = request.GET.get("q", "").strip()
	district = request.GET.get("district", "").strip()
	state = request.GET.get("state", "").strip()

	items = ChurchProfile.objects.filter(is_approved=True, is_public=True).select_related("user")
	if query:
		items = items.filter(
			Q(church_name__icontains=query)
			| Q(pastor_name__icontains=query)
			| Q(user__mobile_number__icontains=query)
		)
	if district:
		items = items.filter(district=district)
	if state:
		items = items.filter(state=state)

	data = [
		{
			"id": row.id,
			"church_name": row.church_name,
			"pastor_name": row.pastor_name,
			"district": row.district,
			"state": row.state,
			"latitude": float(row.latitude) if row.latitude else None,
			"longitude": float(row.longitude) if row.longitude else None,
			"service_name": row.service_name,
			"mobile": row.user.mobile_number,
			"email": row.user.email,
		}
		for row in items[:100]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


# ============================================================================
# MEETINGS/EVENTS
# ============================================================================

@require_GET
def meetings_api(request):
	meeting_type = request.GET.get("meeting_type", "").strip()
	district = request.GET.get("district", "").strip()
	state = request.GET.get("state", "").strip()
	search_query = request.GET.get("q", "").strip()

	items = Meeting.objects.filter(is_published=True).select_related("created_by")
	
	if meeting_type:
		items = items.filter(meeting_type=meeting_type)
	if district:
		items = items.filter(district=district)
	if state:
		items = items.filter(state=state)
	if search_query:
		items = items.filter(
			Q(title__icontains=search_query)
			| Q(description__icontains=search_query)
			| Q(location__icontains=search_query)
		)

	data = [
		{
			"id": row.id,
			"title": row.title,
			"description": row.description[:200],
			"start_date": row.start_date.isoformat() if row.start_date else None,
			"end_date": row.end_date.isoformat() if row.end_date else None,
			"location": row.location,
			"district": row.district,
			"state": row.state,
			"latitude": float(row.latitude) if row.latitude else None,
			"longitude": float(row.longitude) if row.longitude else None,
			"organizer_name": row.organizer_name,
			"estimated_attendance": row.estimated_attendance,
			"meeting_type": row.meeting_type,
		}
		for row in items[:50]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


@require_GET
def meeting_detail_api(request, meeting_id):
	try:
		meeting = Meeting.objects.get(id=meeting_id, is_published=True)
		data = {
			"id": meeting.id,
			"title": meeting.title,
			"description": meeting.description,
			"start_date": meeting.start_date.isoformat() if meeting.start_date else None,
			"end_date": meeting.end_date.isoformat() if meeting.end_date else None,
			"location": meeting.location,
			"district": meeting.district,
			"state": meeting.state,
			"city_area": meeting.city_area,
			"latitude": float(meeting.latitude) if meeting.latitude else None,
			"longitude": float(meeting.longitude) if meeting.longitude else None,
			"organizer_name": meeting.organizer_name,
			"organizer_phone": meeting.organizer_phone if request.user.is_staff or request.user == meeting.created_by else "***",
			"estimated_attendance": meeting.estimated_attendance,
			"meeting_type": meeting.meeting_type,
			"denomination": meeting.denomination,
			"ministry": meeting.ministry,
			"google_map_location": meeting.google_map_location,
			"youtube_link": meeting.youtube_link,
		}
		return JsonResponse({"status": "ok", "data": data})
	except Meeting.DoesNotExist:
		return JsonResponse({"status": "error", "message": "Meeting not found"}, status=404)


# ============================================================================
# JOBS
# ============================================================================

@require_GET
def jobs_api(request):
	job_type = request.GET.get("job_type", "").strip()
	district = request.GET.get("district", "").strip()
	search_query = request.GET.get("q", "").strip()

	items = Job.objects.filter(is_approved=True, is_public=True).select_related("posted_by", "category")
	
	if job_type:
		items = items.filter(job_type=job_type)
	if district:
		items = items.filter(district=district)
	if search_query:
		items = items.filter(
			Q(title__icontains=search_query)
			| Q(description__icontains=search_query)
			| Q(company_name__icontains=search_query)
		)

	data = [
		{
			"id": row.id,
			"title": row.title,
			"company_name": row.company_name,
			"job_type": row.job_type,
			"experience_level": row.experience_level,
			"district": row.district,
			"state": row.state,
			"city_area": row.city_area,
			"salary_min": float(row.salary_min) if row.salary_min else None,
			"salary_max": float(row.salary_max) if row.salary_max else None,
			"currency": row.currency,
			"posted_date": row.posted_date.isoformat() if row.posted_date else None,
		}
		for row in items[:50]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


@require_GET
def job_detail_api(request, job_id):
	try:
		job = Job.objects.get(id=job_id, is_approved=True, is_public=True)
		data = {
			"id": job.id,
			"title": job.title,
			"description": job.description,
			"company_name": job.company_name,
			"job_type": job.job_type,
			"experience_level": job.experience_level,
			"education_level": job.education_level,
			"district": job.district,
			"state": job.state,
			"salary_min": float(job.salary_min) if job.salary_min else None,
			"salary_max": float(job.salary_max) if job.salary_max else None,
			"company_email": job.company_email,
			"company_phone": job.company_phone,
			"company_website": job.company_website,
			"skills_required": job.skills_required,
			"benefits": job.benefits,
			"application_link": job.application_link,
			"deadline": job.deadline.isoformat() if job.deadline else None,
		}
		return JsonResponse({"status": "ok", "data": data})
	except Job.DoesNotExist:
		return JsonResponse({"status": "error", "message": "Job not found"}, status=404)


# ============================================================================
# BUSINESSES
# ============================================================================

@require_GET
def businesses_api(request):
	business_type = request.GET.get("business_type", "").strip()
	district = request.GET.get("district", "").strip()
	search_query = request.GET.get("q", "").strip()

	items = Business.objects.filter(is_approved=True, is_public=True).select_related("posted_by", "category")
	
	if business_type:
		items = items.filter(business_type=business_type)
	if district:
		items = items.filter(district=district)
	if search_query:
		items = items.filter(
			Q(business_name__icontains=search_query)
			| Q(description__icontains=search_query)
			| Q(owner_name__icontains=search_query)
		)

	data = [
		{
			"id": row.id,
			"business_name": row.business_name,
			"business_type": row.business_type,
			"district": row.district,
			"state": row.state,
			"city_area": row.city_area,
			"latitude": float(row.latitude) if row.latitude else None,
			"longitude": float(row.longitude) if row.longitude else None,
			"owner_name": row.owner_name,
			"owner_phone": row.owner_phone,
			"image_url": row.image_url,
		}
		for row in items[:50]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


# ============================================================================
# INSTITUTES
# ============================================================================

@require_GET
def institutes_api(request):
	institute_type = request.GET.get("institute_type", "").strip()
	district = request.GET.get("district", "").strip()
	search_query = request.GET.get("q", "").strip()

	items = Institute.objects.filter(is_approved=True, is_public=True).select_related("posted_by", "category")
	
	if institute_type:
		items = items.filter(institute_type=institute_type)
	if district:
		items = items.filter(district=district)
	if search_query:
		items = items.filter(
			Q(institute_name__icontains=search_query)
			| Q(description__icontains=search_query)
			| Q(principal_name__icontains=search_query)
		)

	data = [
		{
			"id": row.id,
			"institute_name": row.institute_name,
			"institute_type": row.institute_type,
			"district": row.district,
			"state": row.state,
			"principal_name": row.principal_name,
			"website": row.website,
			"established_year": row.established_year,
			"image_url": row.image_url,
		}
		for row in items[:50]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


# ============================================================================
# INCIDENTS
# ============================================================================

@require_GET
def incidents_api(request):
	incident_type = request.GET.get("incident_type", "").strip()
	severity = request.GET.get("severity", "").strip()
	district = request.GET.get("district", "").strip()

	items = Incident.objects.filter(is_approved=True, is_public=True)
	
	if incident_type:
		items = items.filter(incident_type=incident_type)
	if severity:
		items = items.filter(severity=severity)
	if district:
		items = items.filter(district=district)

	data = [
		{
			"id": row.id,
			"title": row.title,
			"incident_type": row.incident_type,
			"severity": row.severity,
			"status": row.status,
			"district": row.district,
			"state": row.state,
			"location": row.location,
			"incident_date": row.incident_date.isoformat() if row.incident_date else None,
		}
		for row in items[:50]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


# ============================================================================
# LOOKUP / REFERENCE DATA
# ============================================================================

@require_GET
def lookups_districts_api(request):
	data = [{"id": code, "name": name} for code, name in DISTRICT_CHOICES]
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_states_api(request):
	data = [{"id": code, "name": name} for code, name in STATE_CHOICES]
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_meeting_types_api(request):
	data = [{"id": code, "name": name} for code, name in MEETING_TYPE_CHOICES]
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_job_types_api(request):
	data = [{"id": code, "name": name} for code, name in JOB_TYPE_CHOICES]
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_business_types_api(request):
	data = [{"id": code, "name": name} for code, name in BUSINESS_TYPE_CHOICES]
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_incident_types_api(request):
	data = [{"id": code, "name": name} for code, name in INCIDENT_TYPE_CHOICES]
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_prayer_categories_api(request):
	data = [{"id": code, "name": name} for code, name in PRAYER_CATEGORY_CHOICES]
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_job_categories_api(request):
	data = list(JobCategory.objects.values("id", "name", "description"))
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_business_categories_api(request):
	data = list(BusinessCategory.objects.values("id", "name", "description"))
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_institute_types_api(request):
	data = [{"id": code, "name": name} for code, name in INSTITUTE_TYPE_CHOICES]
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def lookups_institute_categories_api(request):
	data = list(InstituteCategory.objects.values("id", "name", "description"))
	return JsonResponse({"status": "ok", "data": data})


# ============================================================================
# GALLERY
# ============================================================================

@require_GET
def gallery_categories_api(request):
	data = list(GalleryCategory.objects.filter(is_active=True).values("id", "name", "description"))
	return JsonResponse({"status": "ok", "data": data})


@require_GET
def gallery_images_api(request, category_id):
	try:
		category = GalleryCategory.objects.get(id=category_id, is_active=True)
		images = GalleryImage.objects.filter(category=category, is_active=True)
		data = [
			{
				"id": img.id,
				"title": img.title,
				"description": img.description,
				"image": img.image.url if img.image else None,
				"thumbnail": img.thumbnail.url if img.thumbnail else None,
			}
			for img in images
		]
		return JsonResponse({"status": "ok", "count": len(data), "data": data})
	except GalleryCategory.DoesNotExist:
		return JsonResponse({"status": "error", "message": "Category not found"}, status=404)


# ============================================================================
# PRAYERS
# ============================================================================

@require_GET
def prayers_api(request):
	category = request.GET.get("category", "").strip()
	
	items = Prayer.objects.filter(is_public=True)
	
	if category:
		items = items.filter(category=category)

	data = [
		{
			"id": row.id,
			"title": row.title,
			"description": row.description,
			"category": row.category,
			"submitted_date": row.submitted_date.isoformat() if row.submitted_date else None,
		}
		for row in items[:50]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


# ============================================================================
# LEADERS
# ============================================================================

@require_GET
def leaders_api(request):
	district = request.GET.get("district", "").strip()
	role = request.GET.get("role", "").strip()

	items = Leader.objects.filter(is_approved=True, is_public=True)
	
	if district:
		items = items.filter(district=district)
	if role:
		items = items.filter(role=role)

	data = [
		{
			"id": row.id,
			"name": row.name,
			"role": row.role,
			"district": row.district,
			"organization_name": row.organization_name,
			"email": row.email,
			"phone": row.phone,
			"years_in_ministry": row.years_in_ministry,
			"image_url": row.image_url,
		}
		for row in items[:50]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


# ============================================================================
# MARRIAGES
# ============================================================================

@require_GET
def marriages_api(request):
	gender = request.GET.get("gender", "").strip()
	district = request.GET.get("district", "").strip()

	items = Marriage.objects.filter(is_approved=True, is_public=True)
	
	if gender:
		items = items.filter(gender=gender)
	if district:
		items = items.filter(district=district)

	data = [
		{
			"id": row.id,
			"name": row.name,
			"gender": row.gender,
			"date_of_birth": row.date_of_birth.isoformat() if row.date_of_birth else None,
			"district": row.district,
			"occupation": row.occupation,
			"education": row.education,
			"about_me": row.about_me[:100],
			"interests": row.interests,
			"image_url": row.image_url,
		}
		for row in items[:50]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


# ============================================================================
# NEWS/UPDATES
# ============================================================================

@require_GET
def news_api(request):
	category = request.GET.get("category", "").strip()
	search_query = request.GET.get("q", "").strip()
	
	items = NewsArticle.objects.filter(is_published=True)
	
	if category:
		items = items.filter(category=category)
	if search_query:
		items = items.filter(
			Q(title__icontains=search_query)
			| Q(summary__icontains=search_query)
			| Q(content__icontains=search_query)
		)
	
	data = [
		{
			"id": row.id,
			"title": row.title,
			"slug": row.slug,
			"summary": row.summary,
			"category": row.category if hasattr(row, 'category') else None,
			"published_at": row.published_at.isoformat() if hasattr(row, 'published_at') and row.published_at else None,
		}
		for row in items[:30]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})
