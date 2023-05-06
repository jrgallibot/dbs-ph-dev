# Generated by Django 3.2.13 on 2022-07-14 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('indexer', '0014_alter_website_jsonresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='GSCVerify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(help_text='GSC Email', max_length=200)),
                ('htmlFile', models.TextField(help_text='GSC HTML File Verification', verbose_name='HTML File Name including .html')),
                ('shortnerWebsite', models.URLField(blank=True, help_text='Website that will create the URL Shortners', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GSCVerify', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='website',
            name='JsonResponse',
            field=models.TextField(blank=True, help_text='Add Check Index: at the top to run indexed checker', null=True, verbose_name='Check Index'),
        ),
        migrations.AlterField(
            model_name='website',
            name='jsonFile',
            field=models.TextField(blank=True, help_text='Response From API', null=True, verbose_name='Index Api Result'),
        ),
        migrations.CreateModel(
            name='UrlShortner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pages', models.TextField(blank=True, help_text='List of pages you want to create urlshortners for. 1 Url Per Line', null=True)),
                ('jsonFile', models.TextField(blank=True, help_text='Response From API', null=True, verbose_name='Shortened URLS')),
                ('JsonResponse', models.TextField(blank=True, help_text='Add Check Index: at the top to run indexed checker', null=True, verbose_name='Check Index')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('GSCVerify', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indexer.gscverify')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
