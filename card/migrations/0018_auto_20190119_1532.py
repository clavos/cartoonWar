# Generated by Django 2.1.1 on 2019-01-19 15:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0017_auto_20181214_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='my_following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='my_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
