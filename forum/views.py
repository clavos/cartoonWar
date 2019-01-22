from django.shortcuts import render, redirect
from forum.forms import CommentForm, ArticleForm
from forum.models import Article, Comment
from card.models import UserProfile


def get_all_articles(request):
    form = ArticleForm()
    articles = Article.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.publisher = UserProfile.objects.get(user=request.user)
            article.save()
        return redirect('all_articles')

    return render(request, 'forum/articles.html', {"articles": articles, 'form': form})


def get_one_article(request, **kwargs):
    if request.method == 'GET':
        form = CommentForm()
        article = Article.objects.get(pk=kwargs['pk'])
        comments = article.comment_article.all()
        return render(request, 'forum/detail_article.html', {"article": article, 'comments': comments, 'form': form})
    if request.method == 'POST':
        form = CommentForm(request.POST)
        article = Article.objects.get(pk=kwargs['pk'])
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.publisher = UserProfile.objects.get(user=request.user)
            comment.save()

            return redirect('one_article', pk=kwargs['pk'])
        return redirect('one_article', pk=kwargs['pk'])
