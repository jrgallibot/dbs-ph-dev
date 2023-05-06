# Generated by Django 3.2.13 on 2022-09-03 06:41

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteNetwork', '0005_auto_20220903_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='digitalproperty',
            name='backlinks',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='digitalproperty',
            name='status',
            field=models.CharField(blank=True, default='PBN', max_length=300, null=True),
        ),
    ]
