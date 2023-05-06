# Generated by Django 3.2.13 on 2022-06-23 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(help_text='Your Website', max_length=200)),
                ('indexApi', models.JSONField(help_text='Json Data from Index Api')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='IndexApiUser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('website', models.URLField(help_text='Your Website')),
                ('pages', models.TextField(help_text='list of pages you want to index')),
                ('indexApi', models.JSONField(help_text='Json Data from Index Api')),
                ('jsonFile', models.FileField(help_text='Json Data from Index Api', max_length=500, upload_to='uploads/%Y/%m/%d/')),
                ('indexapi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indexer.indexapi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='WebsiteUser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
