from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者 参数【on_delete】用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题 【models.CharField】为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文 保存大量文本使用 【保存大量文本使用 TextField】
    text = models.TextField()

    # 文章发布时间 参数 【default=timezone.now】 指定其在创建数据时将默认写入当前的时间
    pub_date = models.DateTimeField(default=timezone.now())

    # 文章修改时间 参数 【auto_now=True】 指定每次数据更新时自动写入当前时间
    update = models.DateTimeField(auto_now=True)

    # 文章浏览量
    total_views = models.PositiveIntegerField(default=0)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-pub_date' 表明数据应该以倒序排列
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
        # 获取文章地址

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])