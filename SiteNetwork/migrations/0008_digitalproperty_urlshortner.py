# Generated by Django 3.2.13 on 2022-09-10 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteNetwork', '0007_digitalpropertyclient'),
    ]

    operations = [
        migrations.AddField(
            model_name='digitalproperty',
            name='urlshortner',
            field=models.TextField(blank=True, null=True),
        ),
    ]
