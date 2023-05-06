from django.db import models
import uuid
from indexer.models import IndexApi
from django.utils import timezone
from django.conf import settings

class MobileFriendWeb(models.Model):
    id = models.BigAutoField(primary_key=True)
    api = models.ForeignKey(IndexApi, on_delete=models.CASCADE)
    website = models.URLField(max_length=200, help_text="Your Website")
    pages = models.TextField(help_text='List of pages you want to mobile friendly create. 1 Url Per Line', null=True, blank=True)
    result = models.TextField(blank=True, null=True)
    times_checked = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'mobile_friendly_web'


class MobileFriendlyPages(models.Model):
    id = models.BigAutoField(primary_key=True)
    web = models.ForeignKey('MobileFriendWeb', models.DO_NOTHING)
    url = models.TextField(blank=True, null=True)
    request_screenshot = models.FileField(upload_to='media/mobile_friendly/', null=True, blank=True)
    date_created = models.DateTimeField(blank=True, null=True, default=timezone.now)
    seconds = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    rank = models.IntegerField()
    rank_group = models.IntegerField()
    updated_at = models.DateTimeField(blank=True, null=True)
    date_tracking = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mobile_friendly_pages'