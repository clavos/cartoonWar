# Generated by Django 2.1.3 on 2018-12-14 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_comment_publish_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
