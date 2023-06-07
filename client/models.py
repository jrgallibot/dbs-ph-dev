from django.db import models
from django.conf import settings
from Cloudflare.models import CloudflareModel

class ClientSettings(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.RESTRICT)
	access_token = models.TextField(null=True)


class CloudflareWebsites(models.Model):
	website_id = models.CharField(max_length=255, blank=True, null=True)
	cloudflare = models.ForeignKey(CloudflareModel, on_delete=models.CASCADE)


class ClientComments(models.Model):
	client_site = models.TextField(null = True, blank = True)
	comments = models.TextField(null = True, blank = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.RESTRICT)
	web_id = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'client_comments'


class MaintenanceStatus(models.Model):
	status = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = '_maintenance_mode'