from django import template
from django.db import transaction
from indexer.models import *
from apps.users.models import *
from Cloudflare.models import *
from client.models import *
from django.db.models import Q, Func, F, Value, CharField, Count
from datetime import datetime, date
import json
from urllib.parse import urlparse

register = template.Library()
now = timezone.now()

@register.filter()
def check_permission(user, permission):
	if user.user_permissions.filter(codename=permission).exists():
		return True
	return False


@register.simple_tag
def getapikey_format(data):
	json_data = json.dumps(data)
	print('json_data', json_data)
	return json_data


@register.simple_tag
def json_parser(data):
	if data:
		return json.loads(data)
	return None


@register.simple_tag
def check_sitemap_exist(data):
	data = f'https://{data}/sitemap.xml'
	print(data)
	sitemap = Sitemap.objects.filter(website=data)
	print('sitemap', sitemap)
	return sitemap


@register.simple_tag
def get_domain(data):
	if data:
		domain = urlparse(data).hostname
		return domain
	return None


@register.simple_tag
def getpage_rule(pk):
	data = CloudflarePageRule.objects.filter(resp_url_id = pk)
	return data.first() if data else ''


@register.simple_tag
def get_cloudflare_website(pk):
	if pk:
		return CloudflareWebsites.objects.filter(website_id=pk).first()
	else:
		return None
	

@register.simple_tag
def get_latest_comments(pk):
	data = ClientComments.objects.filter(web_id = pk)
	return data.last().comments if data else ''


@register.simple_tag
def get_post_sched_user(user_id , pk):
	data = ClientPostSched.objects.filter(user_id=user_id, web_id=pk).all()
	return data if data else None


@register.simple_tag
def json_to_date(data):	
	if data:
		return datetime.strptime(data[0:10], '%Y-%m-%d')



@register.simple_tag
def json_to_datetime(data):	
	if data:
		return datetime.strptime(f"{data[0:10]} {data[11:19]}", '%Y-%m-%d %H:%M:%S')
	
	

@register.simple_tag
def get_color_group(web):
	if web:
		group = ClientWebsitePbnGroup.objects.filter(web_id=web).first()
		return group if group else ''
	

@register.filter
def convert_seconds(value):
    value = float(value)
    if value < 60:
        return f"{value:.2f} seconds"
    elif value < 3600:
        minutes = value / 60
        return f"{minutes:.2f} minutes"
    elif value < 86400:
        hours = value / 3600
        return f"{hours:.2f} hours"
    else:
        days = value / 86400
        return f"{days:.2f} days"