from django.urls import path

from .views import (
    about,
    about_subpage,
    admin_dashboard,
    contact,
    dashboard,
    home,
    navigation_group_page,
    privacy_policy,
    terms_conditions,
    job_submission,
    business_submission,
    institute_submission,
    incident_report,
    prayer_submission,
    # Account submission views
    church_timings_submit,
    meetings_submit,
    jobs_submit,
    business_submit,
    institute_submit,
    attacks_submit,
    ads_submit,
    leaders_submit,
    # Service search views
    institutes_search,
    marriages_search,
    jobs_search,
    help_search,
    business_search,
    wings_search,
    organization_search,
    downloads,
)

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("about-us/", about_subpage, name="about-us"),
    path("about-us/<slug:section>/", about_subpage, name="about-section"),
    path("menu/<slug:slug>/", navigation_group_page, name="navigation-group"),
    path("contact/", contact, name="contact"),
    path("privacy-policy/", privacy_policy, name="privacy-policy"),
    path("terms-and-conditions/", terms_conditions, name="terms-and-conditions"),
    path("dashboard/", dashboard, name="dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
    
    # Legacy Service Submissions (kept for backwards compatibility)
    path("services/job-submission/", job_submission, name="job-submission"),
    path("services/business-submission/", business_submission, name="business-submission"),
    path("services/institute-submission/", institute_submission, name="institute-submission"),
    path("services/incident-report/", incident_report, name="incident-report"),
    path("services/prayer-submission/", prayer_submission, name="prayer-submission"),
    
    # Account Menu Submission Forms (11 forms)
    path("account/church-timings/", church_timings_submit, name="church-timings-submit"),
    path("account/meetings/", meetings_submit, name="meetings-submit"),
    path("account/jobs/", jobs_submit, name="jobs-submit"),
    path("account/business/", business_submit, name="business-submit"),
    path("account/institute/", institute_submit, name="institute-submit"),
    path("account/attacks/", attacks_submit, name="attacks-submit"),
    path("account/ads/", ads_submit, name="ads-submit"),
    path("account/leaders/", leaders_submit, name="leaders-submit"),
    path("downloads/", downloads, name="downloads"),
    
    # Services Menu Search Pages (8 search/browse pages)
    path("services/institutes/", institutes_search, name="institutes-search"),
    path("services/marriages/", marriages_search, name="marriages-search"),
    path("services/jobs/", jobs_search, name="jobs-search"),
    path("services/help/", help_search, name="help-search"),
    path("services/business/", business_search, name="business-search"),
    path("services/wings/", wings_search, name="wings-search"),
    path("services/organization/", organization_search, name="organization-search"),
]