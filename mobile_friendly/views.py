from django.http import JsonResponse
from rest_framework import status, authentication
from django.shortcuts import render
import requests
import json
import base64
from django.contrib.auth.decorators import login_required
from indexer.models import IndexApi
# from apps.users.models import *
from dashboard.views import log_history
from asgiref.sync import async_to_sync, sync_to_async
from .models import MobileFriendWeb, MobileFriendlyPages
from django.utils import timezone
import tempfile
import random
from django.core.files.storage import FileSystemStorage
import httpx
import time
import asyncio
import threading
import os
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import transaction
from celery import current_app

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
start_time = time.time()

async def save_to_db(request, pages, api_key, web_id):
	# timeout = httpx.Timeout(connect=None, read=None, write=None, pool=None)
	async with httpx.AsyncClient() as client:
		strings = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!"
		rand_string = ("".join(random.sample(strings, 6)))

		url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'
		global tmp
		tmp = tempfile.NamedTemporaryFile(delete=False)
		if pages:
			for row in pages:
				print('pages ', row.url.rstrip())
				params = {
					'url': row.url.rstrip(),
					'requestScreenshot': 'true',
					'key': api_key
				}
				x = await client.post(url, params=params, timeout=86400)
				data = x.json()
				print(x.status_code)
				if x.status_code == 200 or x.status_code == 201 or x.status_code == 524:

					# Check if status is complete then generate screenshots png.
					if data['testStatus']['status'] == 'COMPLETE':
						print('status complete ........')
						# screen_shots = 'media/mobile_friendly/{}.png'.format(rand_string)
						data_results = ''
						# with open(screen_shots, "wb") as fh:
						# 	fh.write(base64.b64decode(data["screenshot"]["data"]))

						#See the status response
						print("Response code for Google Smartphone is " + str(x)[len(str(x))-5:len(str(x))-2])

						#See the page status result
						print("Page is " + data["mobileFriendliness"])

						#Check if not mobile friendly
						if data["mobileFriendliness"] == "NOT_MOBILE_FRIENDLY":
							for iteration in range (len(data["mobileFriendlyIssues"])):
								data_results += '\n The page has problems with {}. <br>'.format(str(data["mobileFriendlyIssues"][iteration]["rule"]))

						row.status = data["mobileFriendliness"]
						row.seconds = time.time() - start_time
						row.results = data_results
						# row.request_screenshot = 'mobile_friendly/{}.png'.format(rand_string)
						row.save()
						print("--- %s seconds ---" % (time.time() - start_time))
					else:
						row.results = None
						# row.status = 'PAGE_UNREACHABLE'
						row.status = 'NOT_MOBILE_FRIENDLY'
						row.seconds = time.time() - start_time
						# row.request_screenshot = None
						row.save()
						print("--- %s seconds ---" % (time.time() - start_time))

					#Generate results
					with open(tmp.name, 'a') as f:
						f.write('\n Page {}, status {} on {}'.format(row.url.replace('\r',''),
									data["testStatus"]["status"],
									timezone.now()))
				else:
					print("Something went wrong with the API")

			k = ''
			web = ''
			with open(tmp.name) as f:
				for line in f:
					k += line
			print('this is k', k)
			up_mobile = MobileFriendWeb.objects.get(pk = web_id)
			up_mobile.times_checked += 1
			up_mobile.result = k
			up_mobile.save()
			tmp.close()
		else:
			print('No pages to check....')
			return JsonResponse({'data': 'error', 'msg': 'No pages to check.....'})


@login_required()
@csrf_exempt
def check_mobile_friendly_api(request):
	with transaction.atomic():
		try:
			web = MobileFriendWeb.objects.get(pk = request.POST.get('id'))
			pages = MobileFriendlyPages.objects.filter(Q(web_id = web.id) & 
				~Q(status__icontains='MOBILE_FRIENDLY')
				& ~Q(url__isnull=True))
			if pages:
				loop = asyncio.new_event_loop().run_until_complete(save_to_db(request, pages, web.api.indexApi, web.id))
				asyncio.set_event_loop(loop)
				return JsonResponse({'data': 'success', 'msg': 'Pages successfully checking in mobile friendly.'})
			else:
				return JsonResponse({'data': 'error', 'msg': 'No pages to check for mobile friendly method.'})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})


@login_required()
def mobile_friendly_api(request):
	if request.method == 'POST':
		# threads = []
		# api = IndexApi.objects.get(pk = request.POST.get('api_email'))
		# api_key = api.indexApi.replace('""','')
		mob_web = MobileFriendWeb(
			api_id = request.POST.get('api_email'),
			website = request.POST.get('website'),
			pages = request.POST.get('pages'),
			times_checked=0)
		mob_web.save()
		for row in request.POST.get('pages').split('\n'):
			if row.rstrip():
				mob_url = MobileFriendlyPages(
					web_id = mob_web.id,
					url = row.rstrip()
				)
				mob_url.save()
		log_history(request.user.id, 'successfully adding web pages for mobile friendly {}.'.format(request.POST.get('website')))
		return JsonResponse({'data': 'success', 'msg': 'You have successfully adding web pages for mobile friendly.'})

	context = {
		'li': 'mobile_friendly',
		'api': IndexApi.objects.filter(method_id = 3).all(),
	}
	return render(request, 'indexer-admin/admin/mobile_friendly.html', context)


@login_required
def mobile_friendly_api_update(request, pk):
	context = {
		'api': IndexApi.objects.filter(method_id = 3).all(),
		'pk': pk,
		'mob_web': MobileFriendWeb.objects.get(pk = pk)
	}
	return render(request, 'indexer-admin/admin/mobile_friendly_update.html', context)
