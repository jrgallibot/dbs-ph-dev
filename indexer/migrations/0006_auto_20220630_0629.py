# Generated by Django 3.2.13 on 2022-06-30 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexer', '0005_alter_website_pages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexapi',
            name='email',
            field=models.EmailField(help_text='Paste Email Associated with Json Api Above', max_length=200, verbose_name='Json Email'),
        ),
        migrations.AlterField(
            model_name='indexapi',
            name='indexApi',
            field=models.JSONField(help_text='Paste Json Key from Index Api Above', verbose_name='Json Key'),
        ),
    ]
