# Generated by Django 3.2.13 on 2022-06-23 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexer', '0002_auto_20220623_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='user',
        ),
    ]
