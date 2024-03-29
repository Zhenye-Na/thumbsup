# Generated by Django 2.1.7 on 2019-08-19 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='动态内容')),
                ('reply', models.BooleanField(default=False, verbose_name='是否为评论')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('liked', models.ManyToManyField(blank=True, null=True, related_name='liked_news', to=settings.AUTH_USER_MODEL, verbose_name='点赞用户')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread', to='news.News', verbose_name='自关联')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='publisher', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '首页',
                'verbose_name_plural': '首页',
                'ordering': ('-created_at',),
            },
        ),
    ]
