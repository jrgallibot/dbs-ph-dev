# Generated by Django 3.2.13 on 2022-09-10 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cloudflare', '0005_auto_20220910_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloudflaredns',
            name='pageRule',
            field=models.BooleanField(default=False),
        ),
    ]
