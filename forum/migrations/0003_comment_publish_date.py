# Generated by Django 2.1.3 on 2018-12-14 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20181214_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='publish_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]