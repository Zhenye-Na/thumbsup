# Generated by Django 2.2.4 on 2019-08-21 17:18

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=markdownx.models.MarkdownxField(verbose_name='内容'),
        ),
    ]
