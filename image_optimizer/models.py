from django.db import models
import uuid
from indexer.models import IndexApi
from django.utils import timezone
from django.conf import settings

class ImageOptimizer(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField(max_length=200, help_text="Your url")
    entities = models.TextField(help_text='List of pages you want to entities. 1 Url Per Line', null=True, blank=True)
    datetime_added = models.DateTimeField(blank=True, null=True, default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gps_lat = models.TextField(blank=True, null=True)
    gps_long = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'image_optimizer_url'


class ImageOptimizerFile(models.Model):
    id = models.BigAutoField(primary_key=True)
    img_op = models.ForeignKey(ImageOptimizer, on_delete=models.CASCADE)
    gps = models.TextField(blank=True, null=True)
    exif_data = models.TextField(blank=True, null=True)
    image_filename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'image_optimizer_file'