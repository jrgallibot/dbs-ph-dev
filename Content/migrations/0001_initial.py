# Generated by Django 3.2.13 on 2022-09-13 00:57

import ckeditor.fields
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
            name='Spintax7',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('runSpintax', models.BooleanField(default=False)),
                ('topic', models.CharField(blank=True, max_length=300, null=True)),
                ('content1', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('content2', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('content3', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('content4', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('content5', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('content6', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('content7', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Spintax7User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Spintax 7',
                'verbose_name_plural': 'Spintax 7',
            },
        ),
    ]
