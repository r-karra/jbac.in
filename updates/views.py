from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import NewsArticle



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
