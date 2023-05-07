# Generated by Django 3.2.13 on 2022-09-20 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Yacss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('runApp', models.BooleanField(default=False)),
                ('topic', models.CharField(blank=True, max_length=300, null=True)),
                ('questions', models.TextField(blank=True, null=True)),
                ('answers', models.TextField(blank=True, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Yacss_User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Yacss Builder',
                'verbose_name_plural': 'Yacss Builder',
            },
        ),
    ]
