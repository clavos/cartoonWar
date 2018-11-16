# Generated by Django 2.1.1 on 2018-11-08 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_card_card_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_image',
            field=models.ImageField(blank=True, null=True, upload_to='covers/card/%Y/%M/%D/'),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_type',
            field=models.CharField(choices=[('-', '-'), ('Monstre', 'Monstre'), ('Sort', 'Sort')], default='-', max_length=10),
        ),
    ]