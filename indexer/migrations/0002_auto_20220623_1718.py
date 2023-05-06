# Generated by Django 3.2.13 on 2022-06-23 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='indexApi',
            field=models.TextField(help_text='Json Data from Index Api'),
        ),
        migrations.AlterField(
            model_name='website',
            name='jsonFile',
            field=models.TextField(help_text='Json Data from Index Api', max_length=500),
        ),
    ]
