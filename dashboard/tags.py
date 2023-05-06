from django import template
from django.db import transaction
from indexer.models import *
from apps.users.models import *
from Cloudflare.models import *
from django.db.models import Q, Func, F, Value, CharField, Count
from datetime import datetime
import json

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
def getpage_rule(pk):
	data = CloudflarePageRule.objects.filter(resp_url_id = pk)
	return data.first() if data else ''