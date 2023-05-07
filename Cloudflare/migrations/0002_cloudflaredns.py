# Generated by Django 3.2.13 on 2022-08-31 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cloudflare', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudflareDNS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('domain', models.URLField(blank=True, null=True, unique=True)),
                ('oldDNS', models.TextField(blank=True, null=True)),
                ('newDNS', models.TextField(blank=True, null=True)),
                ('getDNS', models.BooleanField(default=False)),
                ('updateDNS', models.BooleanField(default=False)),
                ('resP', models.TextField(blank=True, null=True)),
                ('cloudflaremodel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cloudflare.cloudflaremodel')),
            ],
            options={
                'verbose_name': 'Cloudflare',
                'verbose_name_plural': 'Cloudflare',
            },
        ),
    ]
