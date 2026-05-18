from django.db.models import Prefetch

from .models import NavigationGroup, NavigationItem


def navigation_groups(request):
	item_queryset = NavigationItem.objects.filter(is_active=True)
	if request.user.is_authenticated:
		if not request.user.is_staff:
			item_queryset = item_queryset.filter(staff_only=False)
	else:
		item_queryset = item_queryset.none()

	groups = NavigationGroup.objects.filter(is_active=True).prefetch_related(
		Prefetch("items", queryset=item_queryset)
	)
	return {"navigation_groups": groups}