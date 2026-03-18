from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_seed_about_page_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutpagecontent",
            name="youtube_embed_url",
            field=models.URLField(
                blank=True,
                help_text="Paste a YouTube watch/share/embed URL (e.g. https://youtu.be/... or https://www.youtube.com/watch?v=...).",
            ),
        ),
    ]
