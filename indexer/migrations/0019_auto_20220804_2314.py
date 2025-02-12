# Generated by Django 3.2.13 on 2022-08-04 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexer', '0018_alter_website_jsonresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='index_now',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='website',
            name='indexedRate',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
