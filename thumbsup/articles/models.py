# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from slugify import slugify
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


@python_2_unicode_compatible
class ArticleQuerySet(models.query.QuerySet):
    """自定义 QuerySet, 提高模型可用性"""

    def get_published(self):
        """返回已发表的文章"""
        return self.filter(status="P").select_related('user')

    def get_drafts(self):
        """返回草稿箱的文章"""
        return self.filter(status="D").select_related('user')

    def get_counted_tags(self):
        """统计所有已发表的文章中标签个数大于 0 的文章"""
        tag_dict = {}
        query_set = self.get_published().annotate(tagged=models.Count('tags')).filter(tags__gt=0)

        for obj in query_set:
            for tag in obj.tags.names():
                tag_dict[tag] = tag_dict.get(tag, 0) + 1

        return tag_dict.items()


@python_2_unicode_compatible
class Article(models.Model):
    """文章模型类"""
    STATUS = (('D', 'Draft'), ('P', 'Published'))

    title = models.CharField(max_length=255, null=False, unique=True, verbose_name='标题')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="author", on_delete=models.SET_NULL, verbose_name='作者')
    image = models.ImageField(upload_to='articles_pictures/%Y/%m/%d/', verbose_name='文章图片')
    slug = models.SlugField(max_length=80, null=True, blank=True, verbose_name='(URL)别名')
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='状态')  # 默认存入草稿箱
    content = MarkdownxField(verbose_name='内容')
    edited = models.BooleanField(default=False, verbose_name='是否可编辑')
    tags = TaggableManager(help_text='多个标签使用,(英文)隔开', verbose_name='标签')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            # 根据作者和标题生成文章在 URL 中的别名
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_markdown(self):
        """将 markdown 文本转换成 html"""
        return markdownify(self.content)
