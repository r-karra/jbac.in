from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

admin.site.site_header = "JBAC Administration"
admin.site.site_title = "JBAC Admin"
admin.site.index_title = "Community management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("directory/", include("directory.urls")),
    path("news/", include("updates.urls")),
    path("meetings/", include("meetings.urls")),
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
