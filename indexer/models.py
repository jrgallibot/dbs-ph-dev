from django.conf import settings
from django.db import models
from django.db.models import Q, Func, F, Value, CharField, Count, FloatField, Sum
from ckeditor.fields import RichTextField
from apps.utils.models import BaseModel
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
import httplib2
import json
from django.urls import reverse
import tempfile
import pandas as pd
import time
import requests
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.utils import timezone
from serpapi import GoogleSearch
from django.db import transaction
from celery import current_app
from datetime import datetime
from django.contrib import sitemaps
from django.urls import reverse
import uuid

class RankTracker(models.Model):
	id = models.BigAutoField(primary_key=True)
	keyword = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	is_found = models.IntegerField()
	rank_position = models.IntegerField()
	location = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	time_executed = models.TextField(blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)

	def __str__(self):
		return f"Task ID: {self.task_id} | Keyword: {self.keyword} | Location: {self.location} | Date Created: {self.date_created} "

	def get_total_cost(self):
		cost = RankTrackerHistoryCost.objects.filter(Q(rank__user_id = self.user.id)).aggregate(Sum('cost'))
		return cost['cost__sum']

	class Meta:
		managed = False
		db_table = 'rank_tracker'


class RankTrackerHistoryCost(models.Model):
	id = models.BigAutoField(primary_key=True)
	rank = models.ForeignKey('RankTracker', models.DO_NOTHING)
	cost = models.DecimalField(max_digits=5, decimal_places=2)
	date_updated = models.DateTimeField(blank=True, null=True)
	latest_rank_positions = models.IntegerField()

	class Meta:
		managed = False
		db_table = 'rank_tracker_history'



class Loghistory(models.Model):
	id = models.BigAutoField(primary_key=True)
	descriptions = models.CharField(max_length=255, blank=True, null=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
	datetime_added = models.DateTimeField(blank=True, null=True, default=timezone.now)

	class Meta:
		managed = False
		db_table = 'tbl_loghistory'


class IndexWebTracking(models.Model):
	id = models.BigAutoField(primary_key=True)
	index_web = models.ForeignKey('Website', models.DO_NOTHING)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
	updated_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
	is_right = models.IntegerField(blank=True, null=True, default=1)

	class Meta:
		managed = False
		db_table = 'index_website_dt_tracking'


class IndexApi(BaseModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='IndexApiUser')
	email = models.EmailField(max_length=200, verbose_name='Json Email',
							  help_text="Paste Email Associated with Json Api Above")
	indexApi = models.JSONField(verbose_name='Json Key', help_text="Paste Json Key from Index Api Above")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True, blank=True)
	status = models.IntegerField(blank=True, null=True)
	is_validated = models.IntegerField(blank=True, null=True)
	method = models.ForeignKey('IndexerApiType', models.DO_NOTHING)

	def __str__(self):
		return self.email

	def get_api_usage(self):
		now = datetime.now()
		usage = IndexerApiUsageTracking.objects.filter(api_id = self.id).last()
		if usage:
			return usage.total if usage.date_created.strftime("%d/%m/%Y") == now.strftime("%d/%m/%Y") else 0
		else:
			return 0


class IndexerApiUsageTracking(models.Model):
	api = models.ForeignKey('IndexApi', models.DO_NOTHING)
	total = models.IntegerField(blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'indexer_api_usage_tracking'


class IndexerApiType(models.Model):
	type_method = models.CharField(max_length=255, blank=True, null=True)
	date_added = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.type_method

	class Meta:
		managed = False
		db_table = 'index_api_type'


def insert_event(request_id, response, exception):
	if exception is not None:
		print(f'this is an exception ', exception)
	else:
		print(response)
		k = pd.DataFrame.from_dict(response['urlNotificationMetadata']).iloc[0].tolist()
		print(k)
		with open(tmp.name, 'a') as f:
			f.write('\n ' + ','.join(k))


def insert_event2(request_id, response, exception):
	if exception is not None:
		print(f'this is an exception ', exception)
	else:
		print(response)


def IsIndexed(response, url):
	for count, i in enumerate(response.json.dumps()['organic_results'], 1):
		if url == i['link']:
			return f'Indexed at position {count}'


def numOfDays(date1, date2):
	return (date2 - date1).days


class IndexerPages(models.Model):
	web = models.ForeignKey('Website', models.DO_NOTHING)
	url = models.URLField(max_length=500, blank=True, null=True)
	index_status = models.IntegerField()
	date_added = models.DateTimeField(blank=True, null=True)
	indexed_date = models.DateTimeField(blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	date_tracking = models.TextField(blank=True, null=True)
	rank = models.IntegerField(null=True, blank=True)
	rank_group = models.IntegerField(null=True, blank=True)

	class Meta:
		managed = False
		db_table = 'indexer_pages'


class Website(BaseModel):
	indexapi = models.ForeignKey(IndexApi, on_delete=models.CASCADE)
	website = models.URLField(max_length=200, help_text="Your Website")
	pages = models.TextField(help_text='List of pages you want to index. 1 Url Per Line', null=True, blank=True)
	jsonFile = models.TextField(verbose_name='Index Api Result', help_text="Response From API", null=True, blank=True)
	JsonResponse = models.TextField(verbose_name='Check Indexed Status',
									help_text="Check Index Box Below to run indexed checker", null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	times_indexed = models.IntegerField(default=1, null=True, blank=True)
	updated_at = models.DateTimeField(null=True, blank=True)
	check_index = models.BooleanField(default=False)
	indexedRate = models.IntegerField(default=0, null=True, blank=True)
	index_now = models.BooleanField(default=False)
	times_indexedRate = models.IntegerField(default=0, null=True, blank=True)
	indexedPages = models.TextField(null=True, blank=True)
	NonindexedPages = models.TextField(null=True, blank=True)
	disableIndexing = models.BooleanField(default=False)
	RunIndexer5 = models.BooleanField(default=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def __str__(self):
		return self.website

	def get_absolute_url(self):
		return "/p/%i/" % self.id


	# def save(self, *args, **kwargs):
	#     transaction.on_commit(lambda: current_app.send_task(
	#     	"update_index_rate",
	#     	kwargs={"model_id": self.id},
	#     	ignore_result=False
	#     ))
	#     super().save(*args, **kwargs)

	#     url = self.website

	#     JSON_KEY_FILE = "credentials.json"

	#     SCOPES = ["https://www.googleapis.com/auth/indexing"]
	#     ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

	#     # Authorize credentials
	#     credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.indexapi.indexApi, scopes=SCOPES)
	#     http = credentials.authorize(httplib2.Http())

	#     if self.index_now:
	#         global tmp
	#         tmp = tempfile.NamedTemporaryFile()
	#         service = build('indexing', 'v3', credentials=credentials)
	#         batch = service.new_batch_http_request(callback=insert_event)
	#         for url in self.pages.split('\n'):
	#             batch.add(service.urlNotifications().publish(
	#                 body={"url": url.rstrip(), "type": 'URL_UPDATED'}))
	#         batch.execute()
	#         k = ''
	#         with open(tmp.name) as f:
	#             for line in f:
	#                 print(line)
	#                 k += line
	#         self.jsonFile += k
	#         tmp.close()
	#         self.updated_at = timezone.now()
	#         self.times_indexed += 1
	#         self.index_now = False

	#     elif len(self.pages) < 1:
	#         # Build the request body
	#         content = {}
	#         content['url'] = url
	#         content['type'] = "URL_UPDATED"
	#         json_content = json.dumps(content)

	#         response, content = http.request(ENDPOINT, method="POST", body=json_content)
	#         result = json.loads(content.decode())
	#         self.jsonFile += result
	#         self.updated_at = timezone.now()
	#         self.times_indexed += 1

	#     super().save(*args, **kwargs)


class Sitemap(BaseModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='SitemapUser')
	website = models.URLField(max_length=200, help_text="Website to Crawl Sitemap")
	results = RichTextField(verbose_name='Sitemap Results', help_text="Sitemap Results", null=True, blank=True)
	apikey = models.ForeignKey(IndexApi, on_delete=models.CASCADE)
	is_for_human_check = models.BooleanField(null=True, blank=True)
	sitemap_status = models.IntegerField(blank=True, null=True)
	clicks = models.TextField(blank=True, null=True)
	impressions = models.TextField(blank=True, null=True)
	ctr = models.TextField(blank=True, null=True)
	positions = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.website

	def get_absolute_url(self):
		return reverse("indexer_user:user_site_map", args={str(self.id)})

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)


class SitemapPages(models.Model):
	sitemap = models.ForeignKey('Sitemap', models.DO_NOTHING)
	pages = models.TextField(blank=True, null=True)
	rank = models.IntegerField(blank=True, null=True)
	time_executed = models.CharField(max_length=255, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(blank=True, null=True)
	indexStatusResult = models.CharField(max_length=255, blank=True, null=True)
	conanical_url = models.TextField(blank=True, null=True)
	lastcrawltime = models.DateTimeField(blank=True, null=True)

	@property
	def get_sitemap_lastmod(self):
		get_mod = SitemapModUpdate.objects.filter(sitemap_page_id=self.id).order_by('-id').first()
		return get_mod.last_mod if get_mod else ''

	@property
	def get_sitemap_updated_at(self):
		get_mod = SitemapModUpdate.objects.filter(sitemap_page_id=self.id).order_by('-id').first()
		return get_mod.updated_at if get_mod.updated_at else ''

	class Meta:
		managed = False
		db_table = 'indexer_sitemap_pages'


class SitemapModUpdate(models.Model):
	sitemap_page = models.ForeignKey('SitemapPages', models.DO_NOTHING)
	last_mod = models.DateTimeField(blank=True, null=True)
	updated_at = models.DateTimeField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 'indexer_sitemap_mod_update'


# def sitemap_post_save(sender,instance,*args,**kwargs):

# post_save.connect(sitemap_post_save,sender=Sitemap)
class GSCVerify(BaseModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='GSCVerify')
	email = models.EmailField(max_length=200, help_text="GSC Email")
	htmlFile = models.TextField(verbose_name='HTML File Name including .html', help_text="GSC HTML File Verification")
	shortnerWebsite = models.URLField(max_length=200, help_text="Website that will create the URL Shortners", null=True,
									  blank=True)

	def __str__(self):
		return self.shortnerWebsite

	def save(self, *args, **kwargs):
		url = 'https://m.westfieldstratfordcity2011.com/u/Urls/'
		myobj = {'long_url': 'https://sitemap.google.verify', 'vistor_data': self.htmlFile,
				 'token': '7a0c4b4eb80a72d74d9e6be6e770aefc45ffe103'}
		headers = {'Authorization': 'Token 7a0c4b4eb80a72d74d9e6be6e770aefc45ffe103'}
		x = requests.post(url, json=myobj, headers=headers)

		print(x.text)
		super().save(*args, **kwargs)


class UrlShortner(BaseModel):
	GSCVerify = models.ForeignKey(GSCVerify, on_delete=models.CASCADE)
	pages = models.TextField(help_text='List of pages you want to create urlshortners for. 1 Url Per Line', null=True,
							 blank=True)
	jsonFile = models.TextField(verbose_name='Shortened URLS', help_text="Response From API", null=True, blank=True)
	JsonResponse = models.TextField(verbose_name='Check Index',
									help_text="Add Check Index: at the top to run indexed checker", null=True,
									blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.pages.split('\n')[0]

	def save(self, *args, **kwargs):
		self.JsonResponse = "<table><tr><th>ID</th><th>shorturl</th><<th>Date</th>/tr>"
		for i in self.pages.split('\n'):
			url = 'https://m.westfieldstratfordcity2011.com/u/Urls/'
			myobj = {'long_url': i, 'token': '7a0c4b4eb80a72d74d9e6be6e770aefc45ffe103'}
			headers = {'Authorization': 'Token 7a0c4b4eb80a72d74d9e6be6e770aefc45ffe103'}
			x = requests.post(url, json=myobj, headers=headers)
			shorturl = x.json()['short_url']
			self.jsonFile += f'\n{self.GSCVerify}{shorturl}'
			self.JsonResponse += f" <tr>    <td>{x.json()['id']}</td>    <td>{x.json()['short_url']}</td>  <td>{x.json()['created']}</td>   </tr>"

		super().save(*args, **kwargs)
