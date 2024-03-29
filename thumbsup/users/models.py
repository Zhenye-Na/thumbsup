# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


@python_2_unicode_compatible
class User(AbstractUser):
    """自定义用户模型"""
    nickname = models.CharField(null=True, blank=True, max_length=255, verbose_name='昵称')
    job_title = models.CharField(null=True, blank=True, max_length=50, verbose_name='职称')
    introduction = models.TextField(null=True, blank=True, verbose_name='简介')
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name='头像')
    location = models.CharField(null=True, blank=True, max_length=50, verbose_name='位置')
    personal_url = models.URLField(null=True, blank=True, max_length=255, verbose_name='个人链接')
    weibo = models.URLField(null=True, blank=True, max_length=255, verbose_name='微博链接')
    zhihu = models.URLField(null=True, blank=True, max_length=255, verbose_name='知乎链接')
    github = models.URLField(null=True, blank=True, max_length=255, verbose_name='Github链接')
    linkedin = models.URLField(null=True, blank=True, max_length=255, verbose_name='LinkedIn链接')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        """返回用户名"""
        return self.nickname if self.nickname else self.username
