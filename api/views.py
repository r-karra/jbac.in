from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q

from directory.models import BelieverProfile, ChurchProfile, OrganizationProfile, PastorProfile, StudentProfile
from updates.models import NewsArticle


@require_GET
def platform_stats_api(request):
	data = {
		"believers": BelieverProfile.objects.count(),
		"pastors": PastorProfile.objects.count(),
		"students": StudentProfile.objects.count(),
		"churches": ChurchProfile.objects.count(),
		"organizations": OrganizationProfile.objects.count(),
	}
	return JsonResponse({"status": "ok", "data": data})


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
			"pastor_name": row.pastor_name,
			"church_name": row.church_name,
			"district": row.district,
			"state": row.state,
			"mobile": row.user.mobile_number,
			"email": row.user.email,
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
			| Q(village__icontains=query)
			| Q(user__mobile_number__icontains=query)
		)
	if district:
		items = items.filter(district=district)
	if state:
		items = items.filter(state=state)

	data = [
		{
			"church_name": row.church_name,
			"pastor_name": row.pastor_name,
			"district": row.district,
			"state": row.state,
			"latitude": row.latitude,
			"longitude": row.longitude,
			"mobile": row.user.mobile_number,
			"email": row.user.email,
		}
		for row in items[:100]
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})


@require_GET
def news_api(request):
	items = NewsArticle.objects.filter(is_published=True)[:30]
	data = [
		{
			"title": row.title,
			"slug": row.slug,
			"summary": row.summary,
			"published_at": row.published_at.isoformat(),
		}
		for row in items
	]
	return JsonResponse({"status": "ok", "count": len(data), "data": data})