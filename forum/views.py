from django.shortcuts import render

from forum.models import Article, Comment

def forum(request):
    return render(request, 'forum.html')


def get_all_articles(request):
    articles = Article.objects.all()
    return render(request, 'forum/articles.html', {"articles": articles, "title": "All the articles"})


def get_one_article(request, **kwargs):
    article = Article.objects.get(pk=kwargs['pk'])
    return render(request, 'forum/detail_article.html', {"article": article})
