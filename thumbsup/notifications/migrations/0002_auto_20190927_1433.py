# Generated by Django 2.2.4 on 2019-09-27 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='unread',
            field=models.BooleanField(db_index=True, default=True, verbose_name='未读'),
        ),
    ]
