from django.db import models
from django.conf import settings
from Cloudflare.models import CloudflareModel

class ClientSettings(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.RESTRICT)
	access_token = models.TextField(null=True)


class CloudflareWebsites(models.Model):
	website_id = models.UUIDField(blank=True, null=True)
	page_name = models.CharField(max_length=50, blank=True, null=True, unique=True)
	cloudfare = models.ForeignKey(CloudflareModel, on_delete=models.CASCADE)

	class Meta:
		managed = False
		db_table = 'Cloudflare_websites'