from django.db import migrations


def seed_about_page_content(apps, schema_editor):
    AboutPageContent = apps.get_model("core", "AboutPageContent")

    records = [
        {
            "section_slug": "about-us",
            "menu_title_te": "మా గురించి",
            "menu_title_en": "About Us",
            "page_title_te": "మా గురించి",
            "page_title_en": "About Us",
            "description": "JBAC is a Christian community platform focused on registrations, directory services, and trusted communication.",
            "points_text": "Secure registrations for believers, pastors, students, churches, and organizations.\nBilingual support in Telugu and English.\nAdmin-reviewed visibility for public ministry records.",
            "sort_order": 1,
            "is_active": True,
        },
        {
            "section_slug": "our-help",
            "menu_title_te": "మీకు మా సహాయం",
            "menu_title_en": "Our Help",
            "page_title_te": "మీకు మా సహాయం",
            "page_title_en": "Our Help",
            "description": "We help churches and believers onboard quickly and use JBAC services effectively.",
            "points_text": "Registration support for all role categories.\nDirectory discoverability for approved ministries.\nCommunity updates and communication channels.",
            "sort_order": 2,
            "is_active": True,
        },
        {
            "section_slug": "how-to-use",
            "menu_title_te": "వెబ్ సైట్ ఎలా ఉపయోగించాలి",
            "menu_title_en": "How to Use the Website",
            "page_title_te": "వెబ్ సైట్ ఎలా ఉపయోగించాలి",
            "page_title_en": "How to Use the Website",
            "description": "Follow these steps to use the website productively.",
            "points_text": "Choose the correct registration type.\nLogin with password or OTP.\nUse search and district map features after admin approvals.",
            "sort_order": 3,
            "is_active": True,
        },
        {
            "section_slug": "pastor-guidance-articles",
            "menu_title_te": "చర్చి పాస్టర్ గైడెన్స్ ఆర్టికల్",
            "menu_title_en": "Church Pastor Guidance Articles",
            "page_title_te": "చర్చి పాస్టర్ గైడెన్స్ ఆర్టికల్",
            "page_title_en": "Church Pastor Guidance Articles",
            "description": "Guidance topics for pastors and church leaders.",
            "points_text": "Digital presence for local church outreach.\nMember care and confidentiality practices.\nUsing announcements and prayer support responsibly.",
            "sort_order": 4,
            "is_active": True,
        },
        {
            "section_slug": "add-your-church",
            "menu_title_te": "మీ చర్చి మా వెబ్‌సైట్‌లో ఎలా చేర్చాలి",
            "menu_title_en": "How to Add Your Church to the Website",
            "page_title_te": "మీ చర్చి మా వెబ్‌సైట్‌లో ఎలా చేర్చాలి",
            "page_title_en": "How to Add Your Church to the Website",
            "description": "Register a church profile and include location details for map visibility.",
            "points_text": "Use Church Registration under Register menu.\nFill church name, pastor name, district, and contact details.\nAdd latitude and longitude to appear in district map search.",
            "sort_order": 5,
            "is_active": True,
        },
        {
            "section_slug": "add-announcements",
            "menu_title_te": "క్రైస్తవులకు సంబంధించిన మాటలు చేర్చండి",
            "menu_title_en": "Add Christian Announcements",
            "page_title_te": "క్రైస్తవులకు సంబంధించిన మాటలు చేర్చండి",
            "page_title_en": "Add Christian Announcements",
            "description": "Share verified Christian community announcements through JBAC admin moderation.",
            "points_text": "Prepare title, summary, and event details.\nContact JBAC admins for publishing workflow.\nPublished announcements appear in the News section.",
            "sort_order": 6,
            "is_active": True,
        },
        {
            "section_slug": "prayer-requests",
            "menu_title_te": "క్రైస్తవుల కోసం ప్రార్థన అవసరాలు",
            "menu_title_en": "Prayer Requests for Christians",
            "page_title_te": "క్రైస్తవుల కోసం ప్రార్థన అవసరాలు",
            "page_title_en": "Prayer Requests for Christians",
            "description": "You can share prayer requests with council support channels.",
            "points_text": "Include person name and short prayer context.\nAvoid sensitive private information.\nReach out via contact page for urgent cases.",
            "sort_order": 7,
            "is_active": True,
        },
        {
            "section_slug": "photo-gallery",
            "menu_title_te": "ఫోటో గ్యాలరీ",
            "menu_title_en": "Photo Gallery",
            "page_title_te": "ఫోటో గ్యాలరీ",
            "page_title_en": "Photo Gallery",
            "description": "A curated gallery area for Christian events and ministry moments.",
            "points_text": "Event photos can be shared after moderation.\nUse high-quality images with proper captions.\nCommunity-safe content only.",
            "sort_order": 8,
            "is_active": True,
        },
    ]

    for row in records:
        AboutPageContent.objects.update_or_create(
            section_slug=row["section_slug"],
            defaults=row,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_about_page_content, reverse_code=noop),
    ]
