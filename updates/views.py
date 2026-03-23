from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import NewsArticle
from .forms import NewsSubmissionForm


def news_list(request):
	articles = NewsArticle.objects.filter(is_published=True)
	return render(request, "updates/news_list.html", {"articles": articles})


def news_detail(request, slug):
	article = get_object_or_404(NewsArticle, slug=slug, is_published=True)
	related_articles = NewsArticle.objects.filter(is_published=True).exclude(pk=article.pk)[:3]
	return render(
		request,
		"updates/news_detail.html",
		{"article": article, "related_articles": related_articles},
	)


@login_required(login_url="accounts:login")
@require_http_methods(["GET", "POST"])
def submit_news(request):
	"""Allow registered users to submit news articles."""
	if request.method == "POST":
		form = NewsSubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save(commit=False)
			article.published_at = timezone.now()
			article.is_published = False  # Require admin approval
			article.save()
			messages.success(
				request,
				"విన్నపం చేసిన ధన్యవాదాలు! మీ సమాచారం నిర్వాహక ధృవీకరణ తర్వాత ప్రచురించబడుతుంది.",
			)
			return render(request, "updates/submit_news.html", {"form": NewsSubmissionForm()})
		else:
			messages.error(request, "దయచేసి ఫారమ్‌లోని తప్పులను సరిచేయండి.")
	else:
		form = NewsSubmissionForm()

	return render(request, "updates/submit_news.html", {"form": form})

