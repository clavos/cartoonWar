# Generated by Django 2.1.1 on 2018-11-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0003_deck'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_type',
            field=models.CharField(choices=[('Monstre', 'Monstre'), ('Sort', 'Sort')], default='Monstre', max_length=10),
        ),
    ]
