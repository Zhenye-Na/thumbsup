# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import uuid

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from thumbsup.notifications.views import notification_handler


@python_2_unicode_compatible
class News(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name='publisher', verbose_name='用户')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='thread',
                               verbose_name='自关联')
    content = models.TextField(verbose_name='动态内容')
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_news', verbose_name='点赞用户')
    reply = models.BooleanField(default=False, verbose_name='是否为评论')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '首页'
        verbose_name_plural = verbose_name
        ordering = ('-created_at',)

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        super(News, self).save(*args, **kwargs)

        if not self.reply:
            channel_layer = get_channel_layer()
            payload = {
                "type": "receive",
                "key": "additional_news",
                "actor_name": self.user.username
            }
            async_to_sync(channel_layer.group_send)('notifications', payload)

    def switch_like(self, user):
        """
        点赞/取消点赞

        1) 用户已经点过赞, 则取消点赞
        2) 用户没有点过赞, 点赞
        """
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)
            # 通知楼主
            notification_handler(user, self.user, 'L', self, id_value=str(self.uuid_id), key='social_update')

    def get_parent(self):
        """返回自关联字段的上级记录或者本身"""
        return self.parent if self.parent else self

    def reply_this(self, user, text):
        """
        回复首页动态.

        :param user: 登录的用户
        :param text: 回复的内容
        :return: None
        """
        parent = self.get_parent()

        News.objects.create(
            user=user,
            content=text,
            reply=True,
            parent=parent
        )

        # 通知楼主
        notification_handler(user, parent.user, 'R', parent, id_value=str(parent.uuid_id), key='social_update')

    def get_thread(self):
        """关联到当前记录的所有记录"""
        parent = self.get_parent()
        return parent.thread.all()

    def comment_count(self):
        """获取评论数"""
        return self.get_thread().count()

    def like_count(self):
        """获取点赞数"""
        return self.liked.count()

    def get_likers(self):
        return self.liked.all()
