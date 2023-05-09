from django.db import models
from django.conf import settings
from Cloudflare.models import CloudflareModel

class ClientSettings(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.RESTRICT)
	access_token = models.TextField(null=True)


class CloudflareWebsites(models.Model):
	website_id = models.CharField(max_length=255, blank=True, null=True)
	cloudflare = models.ForeignKey(CloudflareModel, on_delete=models.CASCADE)
