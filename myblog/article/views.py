from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import ArticlePost
from django.core.paginator import Paginator
from . import models
from comment.models import Comment
# Create your views here.



def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    if request.GET.get('order') == 'total_views':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'

    paginator = Paginator(article_list, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {'articles': articles, 'order': order}
    template = loader.get_template('article/list.html')
    return render(request, 'article/list.html', context)


def article_create(request):
    if request.method == 'POST':
        new_article_title = request.POST.get('title')
        new_article_body = request.POST.get('body')
        new_article_author = User.objects.get(id=1)
        models.ArticlePost.objects.create(title=new_article_title, body=new_article_body, author=new_article_author)
        return redirect("article:article_list")
    else:
        return render(request, 'article/create.html')


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    article.total_view += 1
    article.save(update_fields=['total_views'])

    comments = Comment.objects.filter(article=id)

    context = {'article': article}
    context = {'article': article, 'comments': comments}
    return render(request, 'article/detail.html', context)


def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")


# 更新文章
# 提醒用户登录
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("您无权修改此文章！")

    # 判断用户是否为POST提交表单数据
    if request.method == "POST":
        new_article_title = request.POST.get('title')
        new_article_body = request.POST.get('body')
        article.title = new_article_title
        article.body = new_article_body
        article.save()
        return redirect("article:article_detail", id=id)
    else:
        context = {'article': article}
        return render(request, 'article/update.html', context)

