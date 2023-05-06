from urllib.parse import urlparse
from rest_framework import status, authentication
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
import httplib2
import tempfile
import json
from django.shortcuts import render, get_object_or_404
import pandas as pd
from indexer.models import *
from mobile_friendly.models import *
from apps.users.models import *
from django.http import JsonResponse
from django.utils.html import strip_tags
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.utils import timezone
import requests
from serpapi import GoogleSearch
import re
from bs4 import BeautifulSoup
from django.db.models import Q, Func, F, Value, CharField, Count, FloatField, Sum
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from celery import current_app
from indexer import tasks
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from rest_framework.response import Response
import httpx
import time
import asyncio
import threading
import os
from django.contrib.auth.hashers import make_password
from googleapiclient.errors import HttpError

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
start_time = time.time()

def log_history(user, descriptions):
	logs = Loghistory(
		user_id=user,
		descriptions=descriptions
	)
	logs.save()


def insert_event(request_id, response, exception):
	if exception is not None:
		print(f'this is an exception ', exception)
	else:
		print('this is response ', response)
		k = pd.DataFrame.from_dict(response['urlNotificationMetadata']).iloc[0].tolist()
		print("urlNotificationMetadata.url: {}".format(response["urlNotificationMetadata"]["url"]))
		print("urlNotificationMetadata.latestUpdate.url: {}".format(
			response["urlNotificationMetadata"]["latestUpdate"]["url"]))
		print("urlNotificationMetadata.latestUpdate.type: {}".format(
			response["urlNotificationMetadata"]["latestUpdate"]["type"]))
		print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(
			response["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
		print('this is k ', k)
		with open(tmp.name, 'a') as f:
			f.write('\n' + ','.join(k))


def CheckIndexed(response, url):
	for count, i in enumerate(response['organic_results'], 1):
		if url == i['check_url']:
			return '{} {} - {}'.format(url, "Indexed at position", count)


def is_json(myjson):
	try:
		json.loads(myjson)
	except ValueError as e:
		return False
	return True

#REGISTER USER
@login_required
@permission_required('auth.superadmin')
@csrf_exempt
def admin_register_user(request):
	if request.method == 'POST':
		user = CustomUser(
			first_name = request.POST.get('fname'),
			last_name = request.POST.get('lname'),
			middle_name = request.POST.get('mname'),
			email = request.POST.get('email'),
			username = request.POST.get('username'),
			password = make_password(request.POST.get('password')),
			is_superuser = False,
			is_staff = False,
			is_active = True,
			date_joined = datetime.now().date()
		)
		user.save()
		return JsonResponse({'data': 'success', 'msg': 'You have successfully register the user.'})

	context = {
		'li': 'reg_user',
	}
	return render(request, 'indexer-admin/admin/register_users.html', context)


#VIEW USER
@login_required
@permission_required('auth.superadmin')
@csrf_exempt
def admin_view_users(request):
	context = {
		'li': 'user_list',
	}
	return render(request, 'indexer-admin/admin/view-users.html', context)


@login_required
@permission_required('auth.superadmin')
@csrf_exempt
def admin_ranktracker_cost(request):
	context = {
		'li': 'admin_ranktracker_cost',
	}
	return render(request, 'indexer-admin/admin/rank-tracker-cost.html', context)


@login_required
@permission_required('auth.superadmin')
def dashboard_page(request):
	today = timezone.now()
	year = today.strftime("%Y")
	context = {
		'li': 'dashboard',
		'users': CustomUser.objects.all().count(),
		'api': IndexApi.objects.filter(status=1).count(),
		'web': Website.objects.all().count(),
		'index_pages': IndexerPages.objects.filter(index_status=1).count(),
		'none_index_pages': IndexerPages.objects.filter(index_status=0).count(),
		'mobile_friendly': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY').count(),
		'none_mobile_friendly': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY').count(),

		#JANUARY
		'index_jan': IndexerPages.objects.filter(index_status=1, indexed_date__month=1,
												 indexed_date__year=year).count(),
		'none_index_jan': IndexerPages.objects.filter(index_status=0, indexed_date__month=1,
													  indexed_date__year=year).count(),
		'mob_friend_jan': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=1,
													  date_created__year=year).count(),
		'none_mob_friend_jan': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=1,
													  date_created__year=year).count(),

		#FEB
		'index_feb': IndexerPages.objects.filter(index_status=1, indexed_date__month=2,
												 indexed_date__year=year).count(),
		'none_index_feb': IndexerPages.objects.filter(index_status=0, indexed_date__month=2,
													  indexed_date__year=year).count(),
		'mob_friend_feb': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=2,
													  date_created__year=year).count(),
		'none_mob_friend_feb': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=2,
													  date_created__year=year).count(),

		#MARCH
		'index_march': IndexerPages.objects.filter(index_status=1, indexed_date__month=3,
												   indexed_date__year=year).count(),
		'none_index_march': IndexerPages.objects.filter(index_status=0, indexed_date__month=3,
														indexed_date__year=year).count(),
		'mob_friend_march': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=3,
													  date_created__year=year).count(),
		'none_mob_friend_march': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=3,
													  date_created__year=year).count(),

		#APRIL
		'index_april': IndexerPages.objects.filter(index_status=1, indexed_date__month=4,
												   indexed_date__year=year).count(),
		'none_index_april': IndexerPages.objects.filter(index_status=0, indexed_date__month=4,
														indexed_date__year=year).count(),
		'mob_friend_april': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=4,
													  date_created__year=year).count(),
		'none_mob_friend_april': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=4,
													  date_created__year=year).count(),

		#MAY
		'index_may': IndexerPages.objects.filter(index_status=1, indexed_date__month=5,
												 indexed_date__year=year).count(),
		'none_index_may': IndexerPages.objects.filter(index_status=0, indexed_date__month=5,
													  indexed_date__year=year).count(),
		'mob_friend_may': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=5,
													  date_created__year=year).count(),
		'none_mob_friend_may': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=5,
													  date_created__year=year).count(),

		#JUNE
		'index_june': IndexerPages.objects.filter(index_status=1, indexed_date__month=6,
												  indexed_date__year=year).count(),
		'none_index_june': IndexerPages.objects.filter(index_status=0, indexed_date__month=6,
													   indexed_date__year=year).count(),
		'mob_friend_june': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=6,
													  date_created__year=year).count(),
		'none_mob_friend_june': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=6,
													  date_created__year=year).count(),

		#JULY
		'index_july': IndexerPages.objects.filter(index_status=1, indexed_date__month=7,
												  indexed_date__year=year).count(),
		'none_index_july': IndexerPages.objects.filter(index_status=0, indexed_date__month=7,
													   indexed_date__year=year).count(),
		'mob_friend_july': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=7,
													  date_created__year=year).count(),
		'none_mob_friend_july': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=7,
													  date_created__year=year).count(),

		#AUG
		'index_aug': IndexerPages.objects.filter(index_status=1, indexed_date__month=8,
												 indexed_date__year=year).count(),
		'none_index_aug': IndexerPages.objects.filter(index_status=0, indexed_date__month=8,
													  indexed_date__year=year).count(),
		'mob_friend_aug': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=8,
													  date_created__year=year).count(),
		'none_mob_friend_aug': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=8,
													  date_created__year=year).count(),

		#SEP
		'index_sep': IndexerPages.objects.filter(index_status=1, indexed_date__month=9,
												 indexed_date__year=year).count(),
		'none_index_sep': IndexerPages.objects.filter(index_status=0, indexed_date__month=9,
													  indexed_date__year=year).count(),
		'mob_friend_sep': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=9,
													  date_created__year=year).count(),
		'none_mob_friend_sep': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=9,
													  date_created__year=year).count(),

		#OCT
		'index_oct': IndexerPages.objects.filter(index_status=1, indexed_date__month=10,
												 indexed_date__year=year).count(),
		'none_index_oct': IndexerPages.objects.filter(index_status=0, indexed_date__month=10,
													  indexed_date__year=year).count(),
		'mob_friend_oct': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=10,
													  date_created__year=year).count(),
		'none_mob_friend_oct': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=10,
													  date_created__year=year).count(),

		#NOV
		'index_nov': IndexerPages.objects.filter(index_status=1, indexed_date__month=11,
												 indexed_date__year=year).count(),
		'none_index_nov': IndexerPages.objects.filter(index_status=0, indexed_date__month=11,
													  indexed_date__year=year).count(),
		'mob_friend_nov': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=11,
													  date_created__year=year).count(),
		'none_mob_friend_nov': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=11,
													  date_created__year=year).count(),

		#DEC
		'index_dec': IndexerPages.objects.filter(index_status=1, indexed_date__month=12,
												 indexed_date__year=year).count(),
		'none_index_dec': IndexerPages.objects.filter(index_status=0, indexed_date__month=12,
													  indexed_date__year=year).count(),
		'mob_friend_dec': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', date_created__month=12,
													  date_created__year=year).count(),
		'none_mob_friend_dec': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', date_created__month=12,
													  date_created__year=year).count(),
		'mobilefriendly': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY').count(),
		'not_mobilefriendly': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY').count(),
		'sitemap': Sitemap.objects.all().count(),
		'overall_cost': RankTrackerHistoryCost.objects.aggregate(Sum('cost')),
		'cost_perday': RankTrackerHistoryCost.objects.filter(Q(date_updated__day=today.day)).aggregate(Sum('cost')),
	}
	return render(request, 'indexer-admin/admin/dashboard.html', context)


@login_required
@permission_required('auth.superadmin')
def api_type(request):
	if request.method == 'POST':
		check = IndexerApiType.objects.filter(type_method=request.POST.get('method_type'))
		if check:
			return JsonResponse({'data': 'error', 'msg': 'Method api already exist.'})
		else:
			index = IndexerApiType(
				type_method=strip_tags(request.POST.get('method_type')),
				status=1 if request.POST.get('status') else 0
			)
			index.save()
			log_history(request.user.id, 'added new api {}.'.format(request.POST.get('email')))
			return JsonResponse({'data': 'success', 'msg': 'You have successfully added new api keys.'})
	context = {
		'li': 'api_type'
	}
	return render(request, 'indexer-admin/admin/api-type.html', context)


@login_required
@permission_required('auth.superadmin')
def api_type_update(request):
	if request.method == 'POST':
		api_check = IndexerApiType.objects.filter(id=request.POST.get('pk')).first()
		check = IndexerApiType.objects.filter(Q(type_method=request.POST.get('up_method_type')) & ~Q(type_method=api_check.type_method))
		if check:
			return JsonResponse({'data': 'error', 'msg': 'Api type already exist.'})
		else:
			index = IndexerApiType.objects.filter(id=request.POST.get('pk')).update(
				type_method=strip_tags(request.POST.get('up_method_type')),
				status=1 if request.POST.get('up_status') else 0
			)
			log_history(request.user.id, 'updating the api type {}.'.format(request.POST.get('up_method_type')))
			return JsonResponse({'data': 'success', 'msg': 'You have successfully update the api type.'})


@login_required
@permission_required('auth.superadmin')
def dashboard_index_page(request):
	if request.method == 'POST':
		if request.POST.get('api_type') == '1':
			print('here')
			if is_json(request.POST.get('keys')):
				check = IndexApi.objects.filter(Q(email=request.POST.get('email')) & Q(method_id=request.POST.get('api_type')) & Q(user_id=request.user.id))
				if check:
					print('exist na ..')
					return JsonResponse({'data': 'error', 'msg': 'Email api already exist.'})
				else:
					try:
						print('wala pa exist na ..')
						JSON_KEY_FILE = request.POST.get('keys')
						cred = json.loads(JSON_KEY_FILE)
						scopes = [
							'https://www.googleapis.com/auth/webmasters',
							'https://www.googleapis.com/auth/webmasters.readonly'
							]
						end_date = datetime.today().date() - timedelta(days=1)
						start_date = end_date - timedelta(days=20)
						with tempfile.NamedTemporaryFile(delete=False) as temp_file:
							temp_file.write(json.dumps(cred).encode('utf-8'))
							temp_file.flush()
							credentials = service_account.Credentials.from_service_account_file(temp_file.name, scopes=scopes)

						# credentials = service_account.Credentials.from_service_account_file(JSON_KEY_FILE, scopes=scopes)
						service = build('searchconsole','v1',credentials=credentials)

						response = service.sites().list().execute()
						print(response)
						for row in response['siteEntry']:
							print(row)

						if response:
							print('check the response..')
							index = IndexApi(
								user_id=request.user.id,
								email=strip_tags(request.POST.get('email')),
								indexApi=json.loads(request.POST.get('keys')),
								status=1 if request.POST.get('status') else 0,
								method_id=strip_tags(request.POST.get('api_type')),
								is_validated=1
							)
							index.save()
							log_history(request.user.id, 'added new api {}.'.format(request.POST.get('email')))
						return JsonResponse({'data': 'success', 'msg': 'You have successfully added new api keys.'})
					except HttpError as error:
						# Handle the HttpError exception
						print(f'An HTTP error occurred: {error}')
						print(f'Status code: {error.resp.status}')
						print(f'Error content: {error.content}')
						return JsonResponse({'data': 'error', 'msg': f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
														<b>Then How to Fix:</center></b><br> \
														<ul>\
															<li>Please activate the Google Search Console API + Google Index API</li>\
															<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
														</ul>'})
					except Exception as e:
						return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
										<b>Then How to Fix:</center></b><br> \
										<ul>\
											<li>Add Service Account To GSC as Owner</li>\
											<li>Please activate the Google Search Console API + Google Index API</li>\
											<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
										</ul>"})
			else:
				return JsonResponse({'data': 'error', 'msg': 'Invalid api keys.'})
		else:
			print('here too..')
			check = IndexApi.objects.filter(Q(email=request.POST.get('email')) & Q(method_id=request.POST.get('api_type')) & Q(user_id=request.user.id))
			if check:
				return JsonResponse({'data': 'error', 'msg': 'Email api already exist.'})
			else:
				index = IndexApi(
					user_id=request.user.id,
					email=strip_tags(request.POST.get('email')),
					indexApi=request.POST.get('keys').replace('""',''),
					status=1 if request.POST.get('status') else 0,
					method_id=strip_tags(request.POST.get('api_type')),
					is_validated=1
				)
				index.save()
				log_history(request.user.id, 'added new api {}.'.format(request.POST.get('email')))
				return JsonResponse({'data': 'success', 'msg': 'You have successfully added new api keys.'})
		
	context = {
		'li': 'index_api',
		'method': IndexerApiType.objects.filter(status=1).all()
	}
	return render(request, 'indexer-admin/admin/index-api.html', context)


@login_required
@permission_required('auth.superadmin')
def index_api_update(request, pk):
	api_check = IndexApi.objects.filter(id=pk).first()
	if request.method == 'POST':
		if request.POST.get('api_method') == 1:
			if is_json(request.POST.get('index_index_api')):
				check = IndexApi.objects.filter(Q(email=request.POST.get('index_email')) & ~Q(email=api_check.email))
				if check:
					return JsonResponse({'data': 'error', 'msg': 'Email api already exist.'})
				else:
					index = IndexApi.objects.filter(id=pk).update(
						email=strip_tags(request.POST.get('index_email')),
						indexApi=json.loads(request.POST.get('index_index_api')),
						status=1 if request.POST.get('index_status') else 0,
						method_id=strip_tags(request.POST.get('api_method'))
					)
					log_history(request.user.id, 'updating the api {}.'.format(request.POST.get('index_email')))
					return JsonResponse({'data': 'success', 'msg': 'You have successfully update the api keys.'})
			else:
				return JsonResponse({'data': 'error', 'msg': 'Invalid api keys.'})
		else:
			index = IndexApi.objects.filter(id=pk).update(
				email=strip_tags(request.POST.get('index_email')),
				indexApi=request.POST.get('index_index_api').replace('""',''),
				status=1 if request.POST.get('index_status') else 0,
				method_id=strip_tags(request.POST.get('api_method'))
			)
			log_history(request.user.id, 'updating the api {}.'.format(request.POST.get('index_email')))
			return JsonResponse({'data': 'success', 'msg': 'You have successfully update the api keys.'})
	context = {
		'li': 'index_api',
		'method': IndexerApiType.objects.filter(status=1).all(),
		'pk': pk,
		'api': api_check
	}
	return render(request, 'indexer-admin/admin/view-index-api.html', context)


@login_required
@permission_required('auth.superadmin')
@csrf_exempt
def website_add_pages_not_exist(request):
	urls = IndexerPages.objects.values_list('url')
	page_id = IndexerPages.objects.values_list('web_id')
	web = Website.objects.filter(~Q(id__in=page_id))
	count_page = ''
	data_arr = []
	for row in web:
		check = IndexerPages.objects.filter(Q(web_id=row.id) & Q(url__in=urls))
		if not check:
			for data in row.pages.split('\n'):
				print('here', data.rstrip())
				check_page = IndexerPages.objects.filter(Q(web_id=row.id) & Q(url=data.rstrip()))
				if check_page:
					print('duplicate found...')
					pass
				else:
					check_perpage = IndexerPages.objects.filter(Q(web_id=row.id) & Q(url=data.rstrip()))
					if not check_perpage:
						print('naa dri')
						data_arr.append(data)
						newpage = IndexerPages(
							web_id=row.id,
							url=data.rstrip(),
							indexed_date=row.created_at,
							date_added=datetime.now())
						newpage.save()

	print('data_arr', data_arr)
	if len(data_arr) < 1:
		return JsonResponse({'data': 'error', 'msg': 'It seems that there is no pages to add.'})
	else:
		return JsonResponse({'data': 'success', 'msg': 'Successfully added <b>{}  {} in {}  {}</b>.'.format(
			len(data_arr),
			'pages' if len(data_arr) > 1 else 'page',
			web.count(),
			'websites' if web.count() > 1 else 'website')})


@login_required
@permission_required('auth.superadmin')
@csrf_exempt
def check_pages(request):
	try:
		with httpx.Client() as client:
			pages = IndexerPages.objects.filter(web_id=request.POST.get('id'))
			if pages:
				web = Website.objects.get(pk=request.POST.get('id'))
				results = []
				for row in pages:
					if row.index_status != 1:
						if "'" not in row.url:
							print(row.url)
							myobj = {
								'keyword': row.url,
								'url': row.url,
								'location': 'Austin, Texas',
							}
							result = client.post("https://ranktracker.applikuapp.com/dataforseo/api/rank-tracker/", json=myobj,
												   headers={'Content-Type': 'application/json',
															'Authorization': 'Token '
																			 'e279b7682f87000aa8d3915702287ce6020a009e'},
												   timeout=300)
							print(result)
							if result.status_code == 200 or result.status_code == 201:
								data = result.json()
								print('this is data', data)
								print('position', data[0]['position'])
								print('is_found', data[0]['is_found'])
								print('time_executed', data[0]['time_executed'])
								row.index_status = 0 if data[0]['position'] == 300 else 1
								row.rank = data[0]['position']
								row.save()
							else:
								row.index_status = 0
								row.rank = 300
								row.rank_group = 300
								row.save()
								print("Something went wrong with the API")
						else:
							# Invalid URL Status Code = 2
							row.index_status = 2
							row.rank = 300
							row.rank_group = 300
							row.save()
							print('Skipping invalid URL')
				log_history(request.user.id, 'verify the pages {} to index.'.format(row.url))
				return JsonResponse({'data': 'success', 'msg': 'Pages successfully checking.'}, status=200)
			else:
				return JsonResponse({'data': 'error', 'msg': 'Please update the indexing to have a list of urls to index.'})
	except Exception as e:
		# return JsonResponse({'data': 'error', 'msg': str(e)}, status=404)
		return JsonResponse({'data': 'error', 'msg': str(e)})


@login_required
@csrf_exempt
def check_pages_index(request):
	try:
		web = Website.objects.get(pk=request.POST.get('web_id'))
		JSON_KEY_FILE = web.indexapi.indexApi
		print(JSON_KEY_FILE)
		page = IndexerPages.objects.filter(id = request.POST.get('id')).first()
	
		SCOPES = ["https://www.googleapis.com/auth/indexing"]
		ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
		INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

		# Authorize credentials
		credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
		http = credentials.authorize(httplib2.Http())
		service = build('indexing', 'v3', credentials=credentials)
		batch = service.new_batch_http_request(callback=insert_event)
		global tmp
		tmp = tempfile.NamedTemporaryFile(delete=False)
		batch.add(service.urlNotifications().publish(
			body={"url": page.url.rstrip(), "type": 'URL_UPDATED'}))
		batch.execute()
		k = ''
		with open(tmp.name) as f:
			for line in f:
				k += line
		print(page.url)
		numsite_result = f'\n Updated page {page.url} pages on {timezone.now()}'
		web.jsonFile += numsite_result
		web.save()
		tmp.close()
		print('this is result', k)
		return JsonResponse({'data': 'success', 'msg': 'Pages successfully checking in google index method.'})
	except HttpError as error:
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
		return JsonResponse({'data': 'error', 'msg': f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
											<b>Then How to Fix:</center></b><br> \
											<ul>\
												<li>Add Service Account To GSC as Owner make sure to enable</li>\
												<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
											</ul>'})
	except json.decoder.JSONDecodeError as e:
		print("Error decoding JSON:", e)
		return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
											<b>Then How to Fix:</center></b><br> \
											<ul>\
												<li>Add Service Account To GSC as Owner</li>\
												<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
											</ul>"})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
						<b>Then How to Fix:</center></b><br> \
						<ul>\
							<li>Add Service Account To GSC as Owner</li>\
							<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
						</ul>"})


async def save_to_db_mobile_Friendly(request, pages, api_key, web_id):
	# timeout = httpx.Timeout(connect=None, read=None, write=None, pool=None)
	async with httpx.AsyncClient() as client:
		url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'
		global tmp
		tmp = tempfile.NamedTemporaryFile(delete=False)
		if pages:
			print('page ', pages.url.rstrip())
			params = {
				'url': pages.url.rstrip(),
				# 'requestScreenshot': 'true',
				'key': api_key
			}
			x = await client.post(url, params=params, timeout=86400)
			data = x.json()
			print(x.status_code)
			if x.status_code == 200 or x.status_code == 201:

				# Check if status is complete then generate screenshots png.
				if data['testStatus']['status'] == 'COMPLETE':
					print('status complete ........')
					data_results = ''

					#See the status response
					print("Response code for Google Smartphone is " + str(x)[len(str(x))-5:len(str(x))-2])

					#See the page status result
					print("Page is " + data["mobileFriendliness"])

					#Check if not mobile friendly
					if data["mobileFriendliness"] == "NOT_MOBILE_FRIENDLY":
						for iteration in range (len(data["mobileFriendlyIssues"])):
							data_results += '\n The page has problems with {}. <br>'.format(str(data["mobileFriendlyIssues"][iteration]["rule"]))

					pages.status = data["mobileFriendliness"]
					pages.seconds = time.time() - start_time
					pages.results = data_results
					pages.save()
					print("--- %s seconds ---" % (time.time() - start_time))
				else:
					pages.results = None
					# pages.status = 'PAGE_UNREACHABLE'
					pages.status = 'NOT_MOBILE_FRIENDLY'
					pages.seconds = time.time() - start_time
					pages.save()
					print("--- %s seconds ---" % (time.time() - start_time))

				#Generate results
				with open(tmp.name, 'a') as f:
					f.write('\n Page {}, status {} on {}'.format(pages.url.replace('\r',''),
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
			if up_mobile.result:
				up_mobile.result += k
			else:
				up_mobile.result = k
			up_mobile.save()
			tmp.close()
		else:
			print('No pages to check....')
			return JsonResponse({'data': 'error', 'msg': 'No pages to check.....'})


@login_required
@csrf_exempt
def check_pages_if_mobile_friendly(request):
	with transaction.atomic():
		try:
			pages = MobileFriendlyPages.objects.filter(pk= request.POST.get('id')).first()
			if pages.status == 'MOBILE_FRIENDLY':
				return JsonResponse({'data': 'error', 'msg': 'Page are already in mobile friendly. Please check other pages.'})
			else:
				loop = asyncio.new_event_loop().run_until_complete(save_to_db_mobile_Friendly(request, 
					pages, pages.web.api.indexApi, pages.web.id))
				asyncio.set_event_loop(loop)
				return JsonResponse({'data': 'success', 'msg': 'Pages successfully checking in mobile friendly.'})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})

@login_required
@permission_required('auth.superadmin')
def dashboard_indexing_website(request):
	if request.method == 'POST':
		try:
			index = IndexApi.objects.filter(id=request.POST.get('api_email')).first()
			url = request.POST.get('website')
			JSON_KEY_FILE = index.indexApi
			print(JSON_KEY_FILE)
			SCOPES = ["https://www.googleapis.com/auth/indexing"]
			ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
			INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

			# Authorize credentials
			credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
			http = credentials.authorize(httplib2.Http())
			service = build('indexing', 'v3', credentials=credentials)
			batch = service.new_batch_http_request(callback=insert_event)
			data_arr = []
			now = datetime.now()
			if request.POST.get('index_now'):
				global tmp
				tmp = tempfile.NamedTemporaryFile(delete=False)
				for url in request.POST.get('pages').split('\n'):
					data_arr.append(url)
					batch.add(service.urlNotifications().publish(
						body={"url": url.rstrip(), "type": 'URL_UPDATED'}))
				batch.execute()

				# Check total usage of api
				today = datetime.now()
				up_usage = IndexerApiUsageTracking.objects.filter(api_id=request.POST.get('api_email'),
																  date_created__day=today.day,
																  date_created__month=today.month,
																  date_created__year=today.year).first()
				if up_usage:
					if up_usage.total + len(data_arr) <= 200:
						up_usage.total += len(data_arr)
						up_usage.save()

					elif up_usage.total + len(data_arr) >= 200:
						up_usage.total += len(data_arr)
						up_usage.status = 0
						up_usage.save()
						return JsonResponse({'data': 'error', 'msg': 'You have reached the maximum limit of API request '
																	 'for today.'}, status=404)

				else:
					usage = IndexerApiUsageTracking(
						api_id=request.POST.get('api_email'),
						total=len(data_arr),
						status=1
					)
					usage.save()

				k = ''
				web = ''
				with open(tmp.name) as f:
					for line in f:
						k += line
				web = Website(
					indexapi_id=request.POST.get('api_email'),
					website=request.POST.get('website'),
					pages=request.POST.get('pages'),
					times_indexed=1,
					index_now=True,
					jsonFile=k,
				)
				web.save()
				with open(tmp.name) as f:
					index_page = []
					noneindex_page = []
					for line in f:
						pages = line.replace("\n", "")
						if pages.split(",")[0] != '':
							data_arr.append(pages.split(",")[0])
							check_page = IndexerPages.objects.filter(Q(url=pages.split(",")[0]) & Q(web_id=web.id))
							if not check_page:
								index_pages = IndexerPages(
									web_id=web.id,
									url=pages.split(",")[0],
									date_added=timezone.now(),
									indexed_date=pages.split(",")[1],
									index_status=None
								)
								index_pages.save()
							else:
								pass
				tmp.close()
				log_history(request.user.id, 'indexing the website {}.'.format(request.POST.get('website')))

				check_exist_pages =  IndexerPages.objects.filter(web_id=web.id)
				if not check_exist_pages:
					return JsonResponse({'data': 'success', 'title':'Information!', 'msg': "Website successfully saved but the pages is not. To generate all the pages you can click the sync all pages upper\
											 besides in add websites. <br><br> API is Permission denied. Failed to verify the URL ownership: \
											Service Account Not Owner in GSC. Failed to verify the URL ownership! <br><br><center>\
											<b>Then How to Fix:</center></b><br> \
											<ul>\
												<li>Add Service Account To GSC as Owner</li>\
												<li>Double Check API JSON</li>\
											</ul>"})
				else:
					return JsonResponse({'data': 'success', 'msg': 'You have successfully added new website indexing.'})

		except json.decoder.JSONDecodeError as e:
			print("Error decoding JSON:", e)
			return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
					<b>Then How to Fix:</center></b><br> \
					<ul>\
						<li>Add Service Account To GSC as Owner</li>\
						<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
					</ul>"})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
						<b>Then How to Fix:</center></b><br> \
						<ul>\
							<li>Add Service Account To GSC as Owner</li>\
							<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
						</ul>"})

	# Count Website does not exist pages in model
	page_id = IndexerPages.objects.values_list('web_id')
	web = Website.objects.filter(~Q(id__in=page_id))
	context = {
		'li': 'index_web',
		'index_api': IndexApi.objects.filter(method_id = 1).all(),
		'count_web': web.count()
	}
	return render(request, 'indexer-admin/admin/google-index.html', context)


@login_required
@permission_required('auth.superadmin')
def add_pages(request):
	if request.method == 'POST':
		try:
			web = Website.objects.get(pk=request.POST.get('web_id'))
			for row in request.POST.get('url').split('\n'):
				print(row.rstrip())
				check = IndexerPages.objects.filter(Q(web_id=request.POST.get('web_id')) & Q(url=row.rstrip()))
				if check:
					print('duplicate found...')
					pass
				else:
					check_perpage = IndexerPages.objects.filter(Q(web_id=request.POST.get('web_id')) & Q(url=row.rstrip()))
					if not check_perpage:
						newpage = IndexerPages(
							web_id=request.POST.get('web_id'),
							url=row.rstrip(),
							date_added=timezone.now())
						newpage.save()
					log_history(request.user.id, 'add pages {}.'.format(request.POST.get('url')))
			return JsonResponse({'data': 'success', 'msg': 'You have successfully added new page.'})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': 'Error: '+str(e) +'<br><br> For the meantime, developer fixing this issue, in this case please add only urls minimum with 3 pages, untill this error will be fix. Thank you!'})


@login_required
@permission_required('auth.superadmin')
def update_website_index(request, pk):
	if request.method == 'POST':
		print('pk', pk)
		try:
			web = Website.objects.get(pk=pk)
			pages = IndexerPages.objects.filter(Q(web_id=web.id) & (Q(index_status__isnull=True) |
																	Q(index_status=0) |
																	Q(index_status=2)))
			print('this is ', pages.count())
			if pages:
				# transaction.on_commit(lambda: current_app.send_task(
				#   "update_index_rate",
				#   kwargs={"model_id": pk},
				#   ignore_result=False
				# ))
				url = web.website
				JSON_KEY_FILE = web.indexapi.indexApi
				print(JSON_KEY_FILE)

				SCOPES = ["https://www.googleapis.com/auth/indexing"]
				ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
				
				# Authorize credentials
				credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
				http = credentials.authorize(httplib2.Http())
				service = build('indexing', 'v3', credentials=credentials)
				batch = service.new_batch_http_request(callback=insert_event2)
				numsite = ''
				indexYes = 0
				indexNo = 0
				numsite_result = ''
				data_arr = []
				try:
					now = datetime.now()
					for row in pages:
						data_arr.append(row)
						check_dt = IndexerPages.objects.filter(id=row.id, updated_at__isnull=True).first()
						if check_dt:
							print('check_dt')
							batch.add(service.urlNotifications().publish(
								body={"url": row.url.rstrip(), "type": 'URL_UPDATED'}))
							if not check_dt.indexed_date:
								check_dt.indexed_date = timezone.now()
							check_dt.updated_at = timezone.now()
							check_dt.date_tracking = "Last update: {}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
							check_dt.save()
						else:
							print('naa dri')
							count_days = numOfDays(row.updated_at, datetime.today())
							# Check if it is in 6 days above
							if not count_days > 6:
								print('this is count_days ', count_days)
								print('check if it is not beyond in 3 days')
								# Check if it is index today
								if not now.strftime("%d/%m/%Y") == row.updated_at.strftime("%d/%m/%Y"):
									print('check if goes here')
									batch.add(service.urlNotifications().publish(
										body={"url": row.url.rstrip(), "type": 'URL_UPDATED'}))
									result_dt_tracking = "{}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
									upage = IndexerPages.objects.get(pk=row.id)
									if not upage.indexed_date:
										upage.indexed_date = timezone.now()
									track_text = f'\n Last Update {timezone.now()}'
									upage.date_tracking += track_text
									upage.save()
								else:
									print('hellloooooooooooo')
							# Check the index result after 7 days in process of indexing
							elif count_days >= 7:
								print('day 7 of checking in index....')
								if "'" not in row.url:
									myobj = {
										'keyword': f"{row.url}",
										'url': f"{row.url}",
										'location': 'Austin, Texas',
									}
									print(myobj)
									with httpx.Client() as client:
										result = client.post("https://ranktracker.applikuapp.com/dataforseo/api/rank-tracker/", json=myobj,
															headers={'Content-Type': 'application/json',
																		'Authorization': 'Token '
																						'e279b7682f87000aa8d3915702287ce6020a009e'},
															timeout=300)
										print(result)
										if result.status_code == 200 or result.status_code == 201:
											data = result.json()
											print('this is data', data)
											print('position', data[0]['position'])
											print('is_found', data[0]['is_found'])
											print('time_executed', data[0]['time_executed'])
											row.index_status = 0 if data[0]['position'] == 300 else 1
											row.rank = data[0]['position']
											row.save()

											check_data = RankTracker.objects.filter(Q(user_id=request.user.id) & Q(id = check.id) & Q(keyword = check.keyword) & Q(date_created__date=today))
											if not check_data:
												rank = RankTracker(
													keyword = row.url,
													url = row.url,
													location = 'Austin, Texas',
													rank_position = data[0]['position'],
													time_executed = data[0]['time_executed'],
													is_found = data[0]['is_found'],
													user_id = request.user.id)
												rank.save()

												# CREATE AN HISTORY OF RANK TRACKER AND COST PER USED THE API
												check_rank_history = RankTrackerHistoryCost.objects.filter(Q(rank__user_id=request.user.id) & Q(rank_id = rank.id) & Q(latest_rank_positions = data[0]['position']) & Q(date_updated__date=today))
												if not check_rank_history:
													RankTrackerHistoryCost.objects.create(
														rank_id = rank.id,
														latest_rank_positions = data[0]['position'],
														cost = 0.000600,
														date_updated = datetime.now())

										else:
											row.index_status = 0
											row.rank = 300
											row.rank_group = 300
											row.save()
											print("Something went wrong with the API")

											rank = RankTracker(
												keyword = row.url,
												url = row.url,
												location = 'Austin, Texas',
												rank_position = 300,
												time_executed = start_time,
												is_found = 0,
												user_id = request.user.id)
											rank.save()

											# CREATE AN HISTORY OF RANK TRACKER AND COST PER USED THE API
											check_rank_history = RankTrackerHistoryCost.objects.filter(Q(rank__user_id=request.user.id) & Q(rank_id = rank.id) & Q(latest_rank_positions = 300) & Q(date_updated__date=today))
											if not check_rank_history:
												RankTrackerHistoryCost.objects.create(
													rank_id = rank.id,
													latest_rank_positions = 300,
													cost = 0.000600,
													date_updated = datetime.now())
								else:
									# Invalid URL Status Code = 2
									row.index_status = 2
									row.rank_group = 300
									row.updated_at = timezone.now()
									row.save()
									print('Skipping invalid URL')
							else:
								pass

					# Check total usage of api
					today = datetime.now()
					up_usage = IndexerApiUsageTracking.objects.filter(api_id=web.indexapi_id,
																		date_created__day=today.day,
																		date_created__month=today.month,
																		date_created__year=today.year).first()
					if up_usage:
						if up_usage.total + len(data_arr) <= 200:
							up_usage.total += len(data_arr)
							up_usage.save()

						elif up_usage.total + len(data_arr) >= 200:
							up_usage.total += len(data_arr)
							up_usage.status = 0
							up_usage.save()
							return JsonResponse(
								{'data': 'error', 'msg': 'You have reached the maximum limit of API request '
															'for today.'}, status=404)

					else:
						usage = IndexerApiUsageTracking(
							api_id=request.POST.get('api_email'),
							total=len(data_arr),
							status=1
						)
						usage.save()

					batch.execute()
					numsite_result = f'\n Updated {pages.count()} pages on {timezone.now()}'
					print(numsite_result)
					web.jsonFile += numsite_result
					web.updated_at = timezone.now()
					web.times_indexed += 1
					web.indexedRate = int((indexYes/(indexNo+indexYes))*100)
					web.save()
				except:
					web.jsonFile += f'\n Error Updating Indexer Automatically'
					web.save()
				else:
					pass

				# Check if date tracking is exist.
				if web.updated_at is not None:
					check_is_right = IndexWebTracking.objects.filter(index_web_id=pk, is_right=1).first()
					update_tracking = IndexWebTracking(
						index_web_id=pk,
						updated_by_id=request.user.id,
						updated_at=timezone.now(),
						is_right=0 if check_is_right else 1
					)
					update_tracking.save()
				else:
					pass
				log_history(request.user.id, 'update indexing the website {}.'.format(web.website))
				return JsonResponse({'data': 'success', 'msg': 'You have successfully the indexing website.'})
			else:
				return JsonResponse({'data': 'error', 'msg': 'It seems that there are no pages added to index. \
					Please update the indexing to have a list of urls to index.'})
		except json.decoder.JSONDecodeError as e:
			print("Error decoding JSON:", e)
			return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
							<b>Then How to Fix:</center></b><br> \
							<ul>\
								<li>Add Service Account To GSC as Owner</li>\
								<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
							</ul>"})
		except Exception as e:
			print('api error!', str(e))
			return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
							<b>Then How to Fix:</center></b><br> \
							<ul>\
								<li>Add Service Account To GSC as Owner</li>\
								<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
							</ul>"})

	context = {
		'pk': pk,
		'web': Website.objects.get(pk=pk),
		'first_update': Website.objects.filter(id=pk, updated_at__isnull=False).first(),
		'tracking': IndexWebTracking.objects.filter(index_web_id=pk).order_by('-updated_at'),
		'index_api': IndexApi.objects.all(),
		'pages': IndexerPages.objects.filter(web_id=pk)
	}
	return render(request, 'indexer-admin/admin/view_websites_index.html', context)


def get_url_shortner_api(request):
	with httpx.Client() as client:
		result = client.get('https://urlshortner.applikuapp.com/shorten/post/',
							  headers={'Content-Type': 'application/json'})
		json_data = json.loads(result.text)
		return JsonResponse({'data': json_data})


@login_required
@permission_required('auth.superadmin')
def dashboard_url_shortener(request):
	if request.method == 'POST':
		return JsonResponse({'data': 'success', 'msg': 'You have successfully added new api keys.'})
	context = {
		'li': 'url_short',
	}
	return render(request, 'indexer-admin/admin/url_shortener_api.html', context)


@login_required
@permission_required('auth.superadmin')
def dashboard_log_history(request):
	context = {
		'li': 'settings',
	}
	return render(request, 'indexer-admin/admin/log_history.html', context)


def page_not_found(request, exception, template_name="indexer-admin/admin/404.html"):
	response = render_to_response("indexer-admin/admin/404.html")
	response.status_code = 404
	return response


@login_required
@permission_required('auth.superadmin')
def admin_site_map(request):
	if request.method == 'POST':
		user_id = request.user.id
		print('this is site map method..')
		website_url = request.POST.get('website')
		key = request.POST.get('api_key')
		check_human_writer = request.POST.get('check_human_writer')
		api_key = IndexApi.objects.get(pk = request.POST.get('api_key'))
		JSON_KEY_FILE = api_key.indexApi

		if website_url.endswith('.xml'):
			domain = urlparse(website_url).hostname
			if 'www' in domain:
				sc_domain = domain.replace("www.","sc-domain:")
			else:
				sc_domain = 'sc-domain:'+domain
			try:
				scopes = [
					'https://www.googleapis.com/auth/webmasters',
					'https://www.googleapis.com/auth/webmasters.readonly'
				]
				end_date = datetime.today().date() - timedelta(days=1)
				start_date = end_date - timedelta(days=60)
				with tempfile.NamedTemporaryFile(delete=False) as temp_file:
					temp_file.write(json.dumps(JSON_KEY_FILE).encode('utf-8'))
					temp_file.flush()
					credentials = service_account.Credentials.from_service_account_file(temp_file.name, scopes=scopes)

				service = build('searchconsole','v1',credentials=credentials)
				resp = service.sites().list().execute()
				for row in resp['siteEntry']:
					url_1 = website_url
					url_1[-1].replace('/', '')

					url_2 = row['siteUrl']
					if 'sc-domain' in url_2:
						url_2[-1].replace('sc-domain:', '')
						print('1', url_2)
					else:
						url_2[-1].replace('/', '')
						print('2', url_2)
							
					if sc_domain == url_2:
						print(url_1," - ",url_2)
						break
					elif url_1 == url_2:
						print(url_1," - ",url_2)
						break

				request = {
					'url': website_url,
					'startDate': start_date.isoformat(),
					'endDate': end_date.isoformat(),
					'searchType': 'web',
					'rowLimit': 40,
				}
				response = service.searchanalytics().query(siteUrl=url_2, body=request).execute()
				rows = response['rows']
				print(rows)
				site_map = Sitemap(
					website = website_url,
					created_at = datetime.now(),
					user_id=user_id,
					apikey_id=key,
					is_for_human_check= True if check_human_writer else False,
					clicks=rows[0]['clicks'],
					impressions=rows[0]['impressions'],
					ctr=rows[0]['ctr'],
					positions=rows[0]['position'],
					sitemap_status=1)
				site_map.save()
				log_history(user_id, 'successfully adding web pages for site {}.'.format(website_url))
				return JsonResponse({'data': 'success', 'msg': 'You have successfully adding web pages for sitemap.'})
			except HttpError as error:
				# Handle the HttpError exception
				print(f'An HTTP error occurred: {error}')
				print(f'Status code: {error.resp.status}')
				print(f'Error content: {error.content}')
				site_map = Sitemap(
					website = website_url,
					created_at = datetime.now(),
					user_id=user_id,
					apikey_id=key,
					is_for_human_check= True if check_human_writer else False,
					sitemap_status=0)
				site_map.save()
				log_history(user_id, 'successfully adding web pages for site {}.'.format(website_url))
				return JsonResponse({'data': 'error', 'msg': f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
										<b>Then How to Fix:</center></b><br> \
										<ul>\
											<li>Please activate the Google Search Console API + Google Index API</li>\
											<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
										</ul>'})
			except Exception as e:
				site_map = Sitemap(
					website = website_url,
					created_at = datetime.now(),
					user_id=user_id,
					apikey_id=key,
					is_for_human_check= True if check_human_writer else False,
					sitemap_status=0)
				site_map.save()
				log_history(user_id, 'successfully adding web pages for site {}.'.format(website_url))
				return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
							<b>Then How to Fix:</center></b><br> \
							<ul>\
								<li>Add Service Account To GSC as Owner</li>\
								<li>Please activate the Google Search Console API + Google Index API</li>\
								<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
							</ul>"})
		else:
			return JsonResponse({'data': 'error', 'msg': 'String extension is not valid. Please check if it is xml. Thanks!'})
	context = {
		'li': 'site_map',
		'index_api': IndexApi.objects.filter(method_id = 1, is_validated=1).all(),
	}
	return render(request, 'indexer-admin/admin/sitemap.html', context)


@login_required
@permission_required('auth.superadmin')
def admin_site_map_update(request, pk):
	site_map = Sitemap.objects.get(pk = pk)
	context = {
		'site_map': site_map,
		'pk': pk,
		'index_api': IndexApi.objects.filter(method_id = 1).all(),
	}
	return render(request, 'indexer-admin/admin/sitemap_update.html', context)


@login_required
@permission_required('auth.superadmin')
@csrf_exempt
def admin_check_sitemap_lastmod_update(request):
	try:
		sitemap_page_id = request.POST.get('id')
		sitemap_id = request.POST.get('sitemap_id')
		site_map = Sitemap.objects.get(pk = sitemap_id)
		model_website = site_map.website
		from usp.tree import sitemap_tree_for_homepage
		from operator import itemgetter
		tree = sitemap_tree_for_homepage(model_website)
		pagess = list()
		nonepages = list()
		for page in tree.all_pages():
			print(page.url, page.last_modified)
			if page.last_modified == None:
				nonepages.append([page.url, page.last_modified])
			else:
				pagess.append([page.url, page.last_modified])
		pag2 = (sorted(pagess, key=itemgetter(1), reverse=True))
		results = ""
		for i in pag2:
			if "index.html" in i[0]:
				# Check if lastmod already exist with same value
				check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = sitemap_page_id)
				if not check_lastmod_exist:
					SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = sitemap_page_id, updated_at = datetime.now().date())
			else:
				# Check if lastmod already exist with same value
				check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = sitemap_page_id)
				if not check_lastmod_exist:
					SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = sitemap_page_id, updated_at = datetime.now().date())
		for i in nonepages:
			# Check if lastmod already exist with same value
			check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = sitemap_page_id)
			if not check_lastmod_exist:
				SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = sitemap_page_id, updated_at = datetime.now().date())

		page = SitemapPages.objects.get(pk = sitemap_page_id)
		domain = urlparse( page.pages).hostname
		if 'www' in domain:
			sc_domain = domain.replace("www.","sc-domain:")
		else:
			sc_domain = 'sc-domain:'+domain

		scopes = [
			'https://www.googleapis.com/auth/webmasters',
			'https://www.googleapis.com/auth/webmasters.readonly'
		]
		end_date = datetime.today().date() - timedelta(days=1)
		start_date = end_date - timedelta(days=60)
		with tempfile.NamedTemporaryFile(delete=False) as temp_file:
			temp_file.write(json.dumps(site_map.apikey.indexApi).encode('utf-8'))
			temp_file.flush()
			credentials = service_account.Credentials.from_service_account_file(temp_file.name, scopes=scopes)
		service = build('searchconsole','v1',credentials=credentials)
		resp = service.sites().list().execute()
		for row in resp['siteEntry']:
			url_1 = page.pages
			url_1[-1].replace('/', '')

			url_2 = row['siteUrl']
			if 'sc-domain' in url_2:
				url_2[-1].replace('sc-domain:', '')
				print('1', url_2)
			else:
				url_2[-1].replace('/', '')
				print('2', url_2)
					
			if sc_domain == url_2:
				print(url_1," - ",url_2)
				break
			elif url_1 == url_2:
				print(url_1," - ",url_2)
				break

		print('page.pages', page.pages)
		request = {
			'inspectionUrl': page.pages,
			'siteUrl': url_2
		}
		response = service.urlInspection().index().inspect(body=request).execute()
		print('response', response['inspectionResult'])
		inspectionResult = response['inspectionResult']
		try:
			canonical_url = inspectionResult['indexStatusResult']['googleCanonical']
			print(canonical_url)
			print(f'your url: {page.pages} vs canonical url: {canonical_url}')
			page.conanical_url = canonical_url
			page.status = 1 if page.pages == canonical_url else 0
			page.save()
			print("The value of 'google_canonical' is:", canonical_url)
		except KeyError:
			print("The 'google_canonical' key does not exist in 'inspectionResult' dictionary.")

		try:
			coverageState = inspectionResult['indexStatusResult']['coverageState']
			page.indexStatusResult = coverageState if coverageState else None
			page.save()
			print("The value of 'coverageState' is:", coverageState)
		except KeyError:
			page.status = 0
			page.save()
			print("The 'coverageState' key does not exist in 'inspectionResult' dictionary.")

		try:
			lastCrawlTime = inspectionResult['indexStatusResult']['lastCrawlTime']
			page.lastcrawltime = lastCrawlTime if lastCrawlTime else None
			page.save()
			print("The value of 'lastCrawlTime' is:", lastCrawlTime)
		except KeyError:
			page.status = 0
			page.save()
			print("The 'lastCrawlTime' key does not exist in 'inspectionResult' dictionary.")

		return JsonResponse({'data': 'success', 'msg': 'You have successfully check the lastmod update of the url.'})
	except HttpError as error:
		page.status = 0
		page.save()
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
		return JsonResponse({'data': 'error', 'msg': f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
										<b>Then How to Fix:</center></b><br> \
										<ul>\
											<li>Please activate the Google Search Console API + Google Index API</li>\
											<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
										</ul>'})
	except Exception as e:
		page.status = 0
		page.save()
		return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
						<b>Then How to Fix:</center></b><br> \
						<ul>\
							<li>Add Service Account To GSC as Owner</li>\
							<li>Please activate the Google Search Console API + Google Index API</li>\
							<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
						</ul>"})


@login_required()
@permission_required('auth.superadmin')
@csrf_exempt
def admin_check_the_sitemap(request):
	site_map = Sitemap.objects.get(pk = request.POST.get('id'))
	model_website = site_map.website
	from usp.tree import sitemap_tree_for_homepage
	from operator import itemgetter
	tree = sitemap_tree_for_homepage(model_website)
	pagess = list()
	nonepages = list()
	for page in tree.all_pages():
		print(page.url, page.last_modified)
		if page.last_modified == None:
			nonepages.append([page.url, page.last_modified])
		else:
			pagess.append([page.url, page.last_modified])
	pag2 = (sorted(pagess, key=itemgetter(1), reverse=True))
	results = ""
	for i in pag2:
		if "index.html" in i[0]:
			site_pages = SitemapPages(
				sitemap_id = request.POST.get('id'),
				pages =  i[0].replace("index.html", "") if site_map.is_for_human_check == True else i[0],
				time_executed = start_time)
			site_pages.save()
			results += f'\n Url: {i[0].replace("index.html", "") if site_map.is_for_human_check == True else i[0]} - Lastmod: {i[1]}'

			# Check if lastmod already exist with same value
			check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = site_pages.id)
			if not check_lastmod_exist:
				SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = site_pages.id)
		else:
			site_pages = SitemapPages(
				sitemap_id = request.POST.get('id'),
				pages =  os.path.splitext(i[0])[0] if site_map.is_for_human_check == True else i[0],
				time_executed = start_time)
			site_pages.save()
			results += f'\n Url: {os.path.splitext(i[0])[0] if site_map.is_for_human_check == True else i[0]} - Lastmod: {i[1]}'

			# Check if lastmod already exist with same value
			check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = site_pages.id)
			if not check_lastmod_exist:
				SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = site_pages.id)

	for i in nonepages:
		site_pages = SitemapPages(
			sitemap_id = request.POST.get('id'),
			pages = os.path.splitext(i[0])[0],
			time_executed = start_time)
		site_pages.save()

		# Check if lastmod already exist with same value
		check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = site_pages.id)
		if not check_lastmod_exist:
			SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = site_pages.id)
		results += f'\n Url: {os.path.splitext(i[0])[0]} - Lastmod: {i[1]}'
	print('results', results)
	site_map.results = results
	site_map.website = model_website
	site_map.save()
	return JsonResponse({'data': 'success', 'msg': 'You have successfully adding web pages for sitemap.'})

