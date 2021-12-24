from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from article.models import ArticlePost
from . import models


# Create your views here.

# 文章评论
@login_required(login_url='/user/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)
    if request.method == 'POST':
        new_comment_body = request.POST.get('body')
        new_article_user = request.user
        models.Comment.objects.create(article=article, body=new_comment_body, user=new_article_user)
        return redirect(article)
    else:
        return HttpResponse("发表评论仅接受POST请求")