from django.db import models


MEETING_TYPE_CHOICES = [
	("vbs", "VBS"),
	("revival", "ఉద్ధీపన సమావేశాలు"),
	("gospel", "సువార్త సమావేశాలు"),
	("youth", "యూత్ మీటింగ్స్"),
	("leaders", "క్రైస్తవ నాయకుల సమావేశాలు"),
]


DENOMINATION_CHOICES = [
	("assembly-of-god", "Assembly of God"),
	("baptist", "Baptist"),
	("bible-mission", "Bible Mission"),
	("brethren", "Brethren"),
	("church-of-christ", "Church of Christ"),
	("csi", "CSI"),
	("pentecost", "Pentecost"),
	("catholics", "Catholics"),
]


MINISTRY_CHOICES = [
	("american-baptist-mission", "American Baptist Mission"),
	("bible-mission", "Bible Mission"),
	("brethren-assembly", "Brethren Assembly"),
	("calvary-temple", "Calvary Temple"),
	("christ-temple", "Christ Temple"),
	("church-of-christ", "Church of Christ"),
	("full-gospel-fellowship", "Full Gospel Fellowship"),
	("hosanna-ministries", "Hosanna Ministries"),
]


DISTRICT_CHOICES = [
	("alluri-sitharama-raju", "Alluri Sitharama Raju"),
	("anakapalli", "Anakapalli"),
	("anantapur", "Anantapur"),
	("bapatla", "Bapatla"),
	("chittoor", "Chittoor"),
	("east-godavari", "East Godavari"),
	("eluru", "Eluru"),
	("guntur", "Guntur"),
	("kadapa", "Kadapa"),
	("kakinada", "Kakinada"),
	("krishna", "Krishna"),
	("kurnool", "Kurnool"),
	("nellore", "Nellore"),
	("ntr", "NTR"),
	("palnadu", "Palnadu"),
	("prakasam", "Prakasam"),
	("srikakulam", "Srikakulam"),
	("tirupati", "Tirupati"),
	("visakhapatnam", "Visakhapatnam"),
	("vizianagaram", "Vizianagaram"),
	("west-godavari", "West Godavari"),
]


class Meeting(models.Model):
	title = models.CharField(max_length=220)
	description = models.TextField()
	start_date = models.DateField()
	end_date = models.DateField()
	organizer_name = models.CharField(max_length=180)
	estimated_attendance = models.PositiveIntegerField()
	organizer_phone = models.CharField(max_length=20)
	address = models.TextField()
	district = models.CharField(max_length=60, choices=DISTRICT_CHOICES)
	state = models.CharField(max_length=120)
	city_area = models.CharField(max_length=120, blank=True)
	mandal = models.CharField(max_length=120, blank=True)
	village = models.CharField(max_length=120, blank=True)
	meeting_type = models.CharField(max_length=40, choices=MEETING_TYPE_CHOICES, blank=True)
	denomination = models.CharField(max_length=40, choices=DENOMINATION_CHOICES, blank=True)
	ministry = models.CharField(max_length=60, choices=MINISTRY_CHOICES, blank=True)
	google_map_location = models.URLField(blank=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	poster = models.FileField(upload_to="meetings/posters/", blank=True)
	youtube_link = models.URLField(blank=True)
	additional_info = models.TextField(blank=True)
	is_published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["start_date", "title"]

	def __str__(self):
		return f"{self.title} ({self.start_date})"
