# Generated by Django 3.2.13 on 2022-06-23 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexer', '0003_remove_website_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='indexApi',
        ),
    ]
