# Generated by Django 3.2.13 on 2022-07-02 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexer', '0009_website_jsonresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='jsonFile',
            field=models.TextField(blank=True, help_text='Response From API', null=True),
        ),
    ]
