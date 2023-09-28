from django.db import models
from django.conf import settings
from Cloudflare.models import CloudflareModel
import uuid
from django.utils import timezone

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
	web_id = models.TextField(null=True)

	class Meta:
		managed = False
		db_table = 'client_comments'


class ClientPBNLogs(models.Model):
	ipaddress = models.TextField(null = True, blank = True)
	descriptions = models.TextField(null = True, blank = True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.RESTRICT)
	datetime = models.DateTimeField(auto_now_add=True)
	visitors_data = models.TextField(null = True, blank = True)
	timeprocess = models.TextField(null = True, blank = True)

	class Meta:
		managed = False
		db_table = 'client_pbn_logs'

		
class MaintenanceStatus(models.Model):
	status = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = '_maintenance_mode'


class ClientPostSched(models.Model):
	title = models.CharField(max_length=255, blank=True, null=True)
	content = models.TextField(null = True, blank = True)
	slug = models.CharField(max_length=255, null = True, blank = True)
	date = models.DateField(blank=True, null=True)
	date_added = models.DateTimeField(blank=True, null=True, default=timezone.now)
	web_id = models.TextField(null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.RESTRICT)
	status = models.CharField(max_length=255, blank=True, null=True)
	route_id = models.TextField(null=True)
	error_results = models.TextField(null=True)
	

	class Meta:
		managed = False
		db_table = 'client_post_sched'


class ClientPbnGroup(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	color = models.CharField(max_length=255, blank=True, null=True)
	status = models.IntegerField(blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.RESTRICT)

	class Meta:
		managed = False
		db_table = 'client_pbn_group'



class ClientWebsitePbnGroup(models.Model):
	web_id = models.TextField(null=True)
	group = models.ForeignKey(ClientPbnGroup, on_delete=models.CASCADE)
	dateadded = models.DateTimeField(blank=True, null=True, default=timezone.now)

	class Meta:
		managed = False
		db_table = 'client_group_pbn_websites'