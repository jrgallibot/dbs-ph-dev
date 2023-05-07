from urllib.parse import urlparse
import random
from rest_framework import status, authentication
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import BatchHttpRequest
from datetime import datetime, timedelta
import httplib2
import tempfile
import json
from django.shortcuts import render, get_object_or_404, redirect
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
from django.contrib.auth.decorators import login_required
from django.db import transaction
from celery import current_app
from indexer import tasks
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
import httpx
import time
import asyncio
import threading
import os
from indexer.tasks import checking_the_mobile_friendly
from Home.celery import app
from django.contrib.auth.hashers import make_password
from client.models import ClientSettings
from googleapiclient.errors import HttpError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
start_time = time.time()


def log_history(user, descriptions):
	logs = Loghistory(
		user_id=user,
		descriptions=descriptions
	)
	logs.save()

def insert_event_user_side(request_id, response, exception):
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


@login_required
def user_dashboard_page(request):
	today = datetime.today()
	print(today.day)
	year = today.strftime("%Y")
	context = {
		'active_tab': 'dashboard',
		'web': Website.objects.filter(user_id=request.user.id).count(),
		'api': IndexApi.objects.filter(user_id=request.user.id).count(),
		'mobilefriendly': MobileFriendlyPages.objects.filter(status='MOBILE_FRIENDLY', web__user_id=request.user.id).count(),
		'not_mobilefriendly': MobileFriendlyPages.objects.filter(status='NOT_MOBILE_FRIENDLY', web__user_id=request.user.id).count(),
		'sitemap': Sitemap.objects.filter(user_id = request.user.id).count(),
		'cost_perday': RankTrackerHistoryCost.objects.filter(Q(rank__user_id = request.user.id) & Q(date_updated__day=today.day)).aggregate(Sum('cost')),
		'overall_cost': RankTrackerHistoryCost.objects.filter(Q(rank__user_id = request.user.id)).aggregate(Sum('cost'))
	}
	return render(request, 'indexer-user/user-dashboard.html', context)


@login_required
def user_side_index_api(request):
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
		'active_tab': 'index_api',
		'method': IndexerApiType.objects.filter(status=1).all()
	}
	return render(request, 'indexer-user/index-api.html', context)


@login_required
@csrf_exempt
def check_api_to_validate(request):
	with transaction.atomic():
		try:
			print('id', request.POST.get('id'))
			api_data = IndexApi.objects.filter(id=request.POST.get('id')).first()
			JSON_KEY_FILE = api_data.indexApi

			scopes = [
				'https://www.googleapis.com/auth/webmasters',
				'https://www.googleapis.com/auth/webmasters.readonly'
				]
			end_date = datetime.today().date() - timedelta(days=1)
			start_date = end_date - timedelta(days=20)
			with tempfile.NamedTemporaryFile(delete=False) as temp_file:
				temp_file.write(json.dumps(JSON_KEY_FILE).encode('utf-8'))
				temp_file.flush()
				credentials = service_account.Credentials.from_service_account_file(temp_file.name, scopes=scopes)

			# credentials = service_account.Credentials.from_service_account_file(JSON_KEY_FILE, scopes=scopes)
			service = build('searchconsole','v1',credentials=credentials)

			response = service.sites().list().execute()
			print(response)
			for row in response['siteEntry']:
				print(row)

			# Save the database.
			api_data.status = 1
			api_data.is_validated = 1
			api_data.save()
			return JsonResponse({'data': 'success', 'msg': 'Successfully validate the API.'})
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


@login_required
def user_side_index_api_update(request, pk):
	api_check = IndexApi.objects.filter(id=pk).first()
	if request.method == 'POST':
		if request.POST.get('api_method') == '1':
			print('wala dri!')
			if is_json(request.POST.get('index_index_api')):
				check = IndexApi.objects.filter(Q(email=request.POST.get('index_email')) & ~Q(email=api_check.email) 
					& Q(user_id=request.user.id))
				if check:
					return JsonResponse({'data': 'error', 'msg': 'Email api already exist.'})
				else:
					api_key = json.loads(request.POST.get('index_index_api'))
					print('api_key', api_key)
					index = IndexApi.objects.filter(id=pk).update(
						email=strip_tags(request.POST.get('index_email')),
						indexApi=api_key,
						status=1 if request.POST.get('index_status') else 0,
						method_id=strip_tags(request.POST.get('api_method'))
					)
					log_history(request.user.id, 'updating the api {}.'.format(request.POST.get('index_email')))
					return JsonResponse({'data': 'success', 'msg': 'You have successfully update the api keys.'})
			else:
				return JsonResponse({'data': 'error', 'msg': 'Invalid api keys.'})
		else:
			print('naa dri!')
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
	return render(request, 'indexer-user/user-view-index-api.html', context)


@login_required
def user_add_pages(request):
	# if request.method == 'POST':
	try:
		web = Website.objects.get(pk=request.POST.get('web_id'))
		if web:
			for row in request.POST.get('url').split('\n'):
				print(row)
				check = IndexerPages.objects.filter(Q(web_id=request.POST.get('web_id')) & Q(url=row)).first()
				if check:
					print('duplicate found...')
					pass
				else:
					check_perpage = IndexerPages.objects.filter(Q(web_id=request.POST.get('web_id')) & Q(url=row)).first()
					if not check_perpage:
						newpage = IndexerPages(
							web_id=request.POST.get('web_id'),
							url=row.rstrip(),
							date_added=timezone.now())
						newpage.save()
					log_history(request.user.id, 'add pages {}.'.format(request.POST.get('url')))
		return JsonResponse({'data': 'success', 'msg': 'You have successfullprint(JSON_KEY_FILE)y added new page.'})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': 'Error: '+str(e) +'<br><br> For the meantime, developer fixing this issue, in this case please add only urls minimum with 3 pages, untill this error will be fix. Thank you!'})

@login_required
def user_indexing_website(request):
	if request.method == 'POST':
		print('hahhahhhaha')
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
			batch = service.new_batch_http_request(callback=insert_event_user_side)

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
					user_id=request.user.id
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
					return JsonResponse({'data': 'success', 'title':'Good Job!', 'msg': 'You have successfully added new website indexing.'})
					
		except json.decoder.JSONDecodeError as e:
			print("Error decoding JSON:", e)
			return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
												<b>Then How to Fix:</center></b><br> \
												<ul>\
													<li>Add Service Account To GSC as Owner</li>\
													<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
												</ul>"})
		except HttpError as error:
			# Handle the HttpError exception
			print(f'An HTTP error occurred: {error}')
			print(f'Status code: {error.resp.status}')
			print(f'Error content: {error.content}')
			return JsonResponse({'data': 'error', 'msg': f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
								<b>Then How to Fix:</center></b><br> \
								<ul>\
									<li>Add Service Account To GSC as Owner and make sure it is enable</li>\
									<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
								</ul>'})
		except PermissionError as e:
			# handle the permission error
			print("Permission denied. Failed to verify the URL ownership: ", e)
			return JsonResponse({'data': 'error', 'msg': "Permission denied. Failed to verify the URL ownership: "+str(e)})
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
		'active_tab': 'google_index',
		'index_api': IndexApi.objects.filter(method_id = 1, user_id=request.user.id, is_validated=1).all(),
		'count_web': web.count()
	}
	return render(request, 'indexer-user/user-google-index.html', context)


@login_required
@csrf_exempt
def user_google_index_web_delete(request):
	try:
		web_name = Website.objects.filter(id = request.POST.get('id')).first()
		check_pages = IndexerPages.objects.filter(web_id=request.POST.get('id'))
		if check_pages:
			IndexerPages.objects.filter(web_id=request.POST.get('id')).delete()
		web = Website.objects.filter(id = request.POST.get('id')).delete()

		#Logs
		log_history(request.user.id, 'deleting the google index website {}.'.format(web_name.website))
		return JsonResponse({'data': 'success', 'msg': 'Data successfully deleted!'})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': str(e)})


@login_required
@csrf_exempt
def user_google_index_pages_delete(request):
	try:
		check_pages = IndexerPages.objects.filter(id=request.POST.get('id')).first()
		if check_pages:
			IndexerPages.objects.filter(id=request.POST.get('id')).delete()

		#Logs
		log_history(request.user.id, 'deleting the google index page {}.'.format(check_pages.url))
		return JsonResponse({'data': 'success', 'msg': 'Page successfully deleted!'})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': str(e)})


@login_required
@csrf_exempt
def website_user_add_pages_not_exist(request):
	urls = IndexerPages.objects.filter(web__user_id=request.user.id).values_list('url')
	page_id = IndexerPages.objects.filter(web__user_id=request.user.id).values_list('web_id')
	web = Website.objects.filter(~Q(id__in=page_id) & Q(user_id=request.user.id))
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
					pages = data.replace("\n", "")
					if pages.split(",")[0] != '':
						check_perpage = IndexerPages.objects.filter(Q(web_id=row.id) & Q(url=pages.split(",")[0]))
						if not check_perpage:
							print('naa dri')
							data_arr.append(pages.split(",")[0])
							newpage = IndexerPages(
								web_id=row.id,
								url=pages.split(",")[0],
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
def user_update_website_index(request, pk):
	if request.method == 'POST':
		print('pk', pk)
		web = Website.objects.get(pk=pk)
		pages = IndexerPages.objects.filter(Q(web_id=web.id) & (Q(index_status__isnull=True) |
																Q(index_status=0) |
																Q(index_status=2)))
		print('this is ', pages.count())
		try:
			if pages:
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
				today = datetime.now().date()
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
							# Check the index result after 4 days in process of indexing
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
		except HttpError as error:
			# Handle the HttpError exception
			print(f'An HTTP error occurred: {error}')
			print(f'Status code: {error.resp.status}')
			print(f'Error content: {error.content}')
			return JsonResponse({'data': 'error', 'msg': f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
								<b>Then How to Fix:</center></b><br> \
								<ul>\
									<li>Add Service Account To GSC as Owner and make sure it is enable</li>\
									<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
								</ul>'})
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
		'index_api': IndexApi.objects.filter(user_id=request.user.id, is_validated=1).all(),
		'pages': IndexerPages.objects.filter(web_id=pk)
	}
	return render(request, 'indexer-user/user_view_websites_index.html', context)


@login_required
@csrf_exempt
def user_check_pages(request):
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
								row.save()
								print("Something went wrong with the API")
						else:
							# Invalid URL Status Code = 2
							row.index_status = 2
							row.rank = 300
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
def user_mobile_friendly(request):
	if request.method == 'POST':
		print('this is user_mobile_friendly')
		mob_web = MobileFriendWeb(
			api_id = request.POST.get('api_email'),
			website = request.POST.get('website'),
			pages = request.POST.get('pages'),
			times_checked=0,
			user_id=request.user.id)
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
		'active_tab': 'mobile_friendly',
		'api': IndexApi.objects.filter(user_id=request.user.id, method_id = 3).all(),
	}
	return render(request, 'indexer-user/user-mobile-friendly.html', context)


@login_required
def user_mobile_friendly_update(request, pk):
	context = {
		'api': IndexApi.objects.filter(user_id=request.user.id, method_id = 3).all(),
		'pk': pk,
		'mob_web': MobileFriendWeb.objects.get(pk = pk)
	}
	return render(request, 'indexer-user/user-mobile-friendly-update.html', context)


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
				x = await client.post(url, params=params, timeout=100000)
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


def checking_the_mobilefriendly(request, pages, api_key, web_id):
	print('ni abot ko dri !')
	while True:
		url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'
		global tmp
		tmp = tempfile.NamedTemporaryFile(delete=False)
		if pages:
			for row in pages:
				print('pages ', row.url.rstrip())
				params = {
					'url': row.url.rstrip(),
					# 'requestScreenshot': 'true',
					'key': api_key
				}
				x = httpx.post(url, params=params, timeout=1800)
				data = x.json()
				print('this is ', x.status_code)
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
			break
		time.sleep(3)
	return True


@login_required()
@csrf_exempt
def user_check_mobile_friendly_api(request):
	from apscheduler.schedulers.background import BackgroundScheduler
	scheduler = BackgroundScheduler()
	print('this is pk', request.POST.get('id'))
	threads = []
	web = MobileFriendWeb.objects.get(pk = request.POST.get('id'))
	pages = MobileFriendlyPages.objects.filter(Q(web_id = web.id) & 
			~Q(status__icontains='MOBILE_FRIENDLY')
			& ~Q(url__isnull=True))
	if pages:
		scheduler.add_job(checking_the_mobilefriendly(request, pages, web.api.indexApi, web.id), 'interval', seconds=15)
		scheduler.start()
		# transaction.on_commit(lambda: current_app.send_task(
		#   "checking_the_mobile_friendly",
		# 	kwargs={"web_id": web.id}
		# ))
		# t = threading.Thread(target=checking_the_mobilefriendly, args=(request, pages, web.api.indexApi, web.id), daemon=True)
		# t.start()
		# threads.append(t)
		# for thread in threads:
		# 	thread.join()
	return JsonResponse({'data': 'success'})
	

@login_required
def user_site_map(request):
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
			
			print('sc_admin', sc_domain)
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
				print('url_2', url_2)
				response = service.searchanalytics().query(siteUrl=url_2, body=request).execute()
				print('response', response)
				if "rows" in response:
					rows = response['rows']
					print('rows', rows)
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
				else:
					site_map = Sitemap(
						website = website_url,
						created_at = datetime.now(),
						user_id=user_id,
						apikey_id=key,
						is_for_human_check= True if check_human_writer else False,
						sitemap_status=0)
					site_map.save()
					log_history(user_id, 'successfully adding web pages for site {}.'.format(website_url))
					return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str("<b>User does not have sufficient permission for site</b>")+ "<br><br><center>\
							<b>Then How to Fix:</center></b><br> \
							<ul>\
								<li>Add Service Account To GSC as Owner</li>\
								<li>Please activate the Google Search Console API + Google Index API</li>\
								<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
							</ul>"})
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
		'active_tab': 'site_map',
		'index_api': IndexApi.objects.filter(method_id = 1, user_id=request.user.id, is_validated=1).all(),
	}
	return render(request, 'indexer-user/user-site-map.html', context)


@login_required
@csrf_exempt
def user_check_site_url(request):
	print(request.POST.get('id'))
	user_id = request.user.id
	site_map = Sitemap.objects.filter(id = request.POST.get('id')).first()
	JSON_KEY_FILE = site_map.apikey.indexApi
	website_url = site_map.website

	#Check the domain of the webiste
	domain = urlparse(website_url).hostname
	if 'www' in domain:
		sc_domain = domain.replace("www.","sc-domain:")
	else:
		sc_domain = 'sc-domain:'+domain

	#Try Catch the error exeption of this method..	
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
		site_map.clicks = rows[0]['clicks']
		site_map.impressions = rows[0]['impressions']
		site_map.ctr = rows[0]['ctr']
		site_map.positions = rows[0]['position']
		site_map.sitemap_status = 1
		site_map.save()
		log_history(user_id, 'successfully updating web pages for site {}.'.format(website_url))
		return JsonResponse({'data': 'success', 'msg': 'You have successfully adding web pages for sitemap.'})
	except HttpError as error:
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
		site_map.sitemap_status = 0
		site_map.save()
		log_history(user_id, 'successfully updating web pages for site {}.'.format(website_url))
		return JsonResponse({'data': 'error', 'msg': f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
								<b>Then How to Fix:</center></b><br> \
								<ul>\
									<li>Please activate the Google Search Console API + Google Index API</li>\
									<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
								</ul>'})
	except Exception as e:
		site_map.sitemap_status = 0
		site_map.save()
		log_history(user_id, 'successfully updating web pages for site {}.'.format(website_url))
		return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
					<b>Then How to Fix:</center></b><br> \
					<ul>\
						<li>Add Service Account To GSC as Owner</li>\
						<li>Please activate the Google Search Console API + Google Index API</li>\
						<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
					</ul>"})

@login_required
@csrf_exempt
def user_sitemap_web_delete(request):
	try:
		sitemap_name = Sitemap.objects.filter(id = request.POST.get('id')).first()
		check_pages = SitemapPages.objects.filter(sitemap_id=request.POST.get('id'))
		if check_pages:
			for row in check_pages:
				SitemapModUpdate.objects.filter(sitemap_page_id = row).delete()
			SitemapPages.objects.filter(sitemap_id=request.POST.get('id')).delete()
		sitemap = Sitemap.objects.filter(id = request.POST.get('id')).delete()

		#Logs
		log_history(request.user.id, 'deleting the sitemap website {}.'.format(sitemap_name.website))
		return JsonResponse({'data': 'success', 'msg': 'Data successfully deleted!'})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': str(e)})

@login_required
@csrf_exempt
def user_sitemap_pages_delete(request):
	try:
		check_pages = SitemapPages.objects.filter(id=request.POST.get('id')).first()
		if check_pages:
			SitemapModUpdate.objects.filter(sitemap_page_id = check_pages.id).delete()
			SitemapPages.objects.filter(id=request.POST.get('id')).delete()

		#Logs
		log_history(request.user.id, 'deleting the sitemap page {}.'.format(check_pages.pages))
		return JsonResponse({'data': 'success', 'msg': 'Page successfully deleted!'})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': str(e)})

@login_required
def user_site_map_update(request, pk):
	site_map = Sitemap.objects.get(pk = pk)
	context = {
		'site_map': site_map,
		'pk': pk,
		'index_api': IndexApi.objects.filter(method_id = 1, user_id=request.user.id).all(),
	}
	return render(request, 'indexer-user/user-site-map-update.html', context)
	

def checking_the_sitemap_pages(request, pk, site_map, model_website, JSON_KEY_FILE):
	print('ni abot ko dri !')
	print(JSON_KEY_FILE)
	while True:
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
		results_indexer = ""
		for i in pag2:
			if "index.html" in i[0]:
				print('naa dri !')
				chck_page = SitemapPages.objects.filter(Q(sitemap_id = pk) & 
					    Q(pages = i[0].replace("index.html", "") if site_map.is_for_human_check == True else i[0]))
				if not chck_page:
					site_pages = SitemapPages(
						sitemap_id = pk,
						pages =  i[0].replace("index.html", "") if site_map.is_for_human_check == True else i[0],
						time_executed = start_time)
					site_pages.save()
					results += f'\n Url: {i[0].replace("index.html", "") if site_map.is_for_human_check == True else i[0]} - Lastmod: {i[1]}'
					results_indexer += f'\n {i[0].replace("index.html", "") if site_map.is_for_human_check == True else i[0]}'

					# Check if lastmod already exist with same value
					check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = site_pages.id)
					if not check_lastmod_exist:
						SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = site_pages.id)
				else:
					print('page is duplicated.')
			else:
				print('basin naa dri !')
				chck_page = SitemapPages.objects.filter(Q(sitemap_id = pk) & 
					    Q(pages = os.path.splitext(i[0])[0] if site_map.is_for_human_check == True else i[0]))
				if not chck_page:
					site_pages = SitemapPages(
						sitemap_id = pk,
						pages =  os.path.splitext(i[0])[0] if site_map.is_for_human_check == True else i[0],
						time_executed = start_time)
					site_pages.save()
					results += f'\n Url: {os.path.splitext(i[0])[0] if site_map.is_for_human_check == True else i[0]} - Lastmod: {i[1]}'
					results_indexer += f'\n {os.path.splitext(i[0])[0] if site_map.is_for_human_check == True else i[0]}'

					# Check if lastmod already exist with same value
					check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = site_pages.id)
					if not check_lastmod_exist:
						SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = site_pages.id)
				else:
					print('page is duplicated.')
		for i in nonepages:
			print('wala sulod !')
			chck_page = SitemapPages.objects.filter(Q(sitemap_id = pk) & Q(pages = os.path.splitext(i[0])[0]))
			if not chck_page:
				site_pages = SitemapPages(
					sitemap_id = pk,
					pages = os.path.splitext(i[0])[0],
					time_executed = start_time)
				site_pages.save()

				# Check if lastmod already exist with same value
				check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = site_pages.id)
				if not check_lastmod_exist:
					SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = site_pages.id)
				results += f'\n Url: {os.path.splitext(i[0])[0]} - Lastmod: {i[1]}'
			else:
				print('page is duplicated.')

		try:
			SCOPES = ["https://www.googleapis.com/auth/indexing"]
			ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
			INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
			global tmp
			credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
			http = credentials.authorize(httplib2.Http())
			service = build('indexing', 'v3', credentials=credentials)
			batch = service.new_batch_http_request(callback=insert_event_user_side)
			tmp = tempfile.NamedTemporaryFile(delete=False)
			# CHECK IN GOOGLE INDEX THE SITEMAP PAGES
			for i in pag2:
				if "index.html" in i[0]:
					batch.add(service.urlNotifications().publish(
							body={"url": i[0].replace("index.html", "") if site_map.is_for_human_check == True else i[0], 
							"type": 'URL_UPDATED'}))
				else:
					batch.add(service.urlNotifications().publish(
							body={"url": os.path.splitext(i[0])[0] if site_map.is_for_human_check == True else i[0], 
							"type": 'URL_UPDATED'}))
			batch.execute()
			print('im here......')
			# k = ''
			# web = ''
			# with open(tmp.name) as f:
			# 	for line in f:
			# 		k += line
			# web = Website(
			# 	indexapi_id=site_map.apikey.id,
			# 	website=site_map.website,
			# 	pages=results_indexer,
			# 	times_indexed=1,
			# 	index_now=True,
			# 	jsonFile=k,
			# 	user_id=request.user.id
			# )
			# web.save()
			# with open(tmp.name) as f:
			# 	index_page = []
			# 	noneindex_page = []
			# 	for line in f:
			# 		pages = line.replace("\n", "")
			# 		if pages.split(",")[0] != '':
			# 			data_arr.append(pages.split(",")[0])
			# 			check_page = IndexerPages.objects.filter(Q(url=pages.split(",")[0]) & Q(web_id=web.id))
			# 			if not check_page:
			# 				index_pages = IndexerPages(
			# 					web_id=web.id,
			# 					url=pages.split(",")[0],
			# 					date_added=timezone.now(),
			# 					indexed_date=pages.split(",")[1],
			# 					index_status=None
			# 				)
			# 				index_pages.save()
			# 			else:
			# 				pass
			# tmp.close()
			# END OF GOOGLE INDEX EXECUTE
		except json.decoder.JSONDecodeError as e:
			print("Error decoding JSON:", e)
		except Exception as e:
			print('Index Api error!', e)
			
		print('results', results)
		site_map.results = results
		site_map.website = model_website
		site_map.save()
		break
		time.sleep(3)
	return True


@login_required()
@csrf_exempt
def user_check_the_sitemap(request):
	site_map = Sitemap.objects.get(pk = request.POST.get('id'))
	model_website = site_map.website
	JSON_KEY_FILE = site_map.apikey.indexApi
	threads = []
	if site_map:
		t = threading.Thread(target=checking_the_sitemap_pages, args=(request, request.POST.get('id'), site_map, model_website, JSON_KEY_FILE), daemon=True)
		t.start()
		threads.append(t)
		for thread in threads:
			thread.join()
	return JsonResponse({'data': 'success'})


@login_required()
@csrf_exempt
def user_check_the_sitemap_duplicated_delete(request):
	try:
		duplicates = SitemapPages.objects.values('pages').annotate(count=Count('pages')).filter(count__gt=1, 
						sitemap_id=request.POST.get('pk'))
		for duplicate in duplicates:
			pages = SitemapPages.objects.filter(pages=duplicate['pages'], sitemap_id=request.POST.get('pk')).order_by('id')
			# keep the first page and delete the rest
			if pages.query.low_mark or pages.query.high_mark:
				pages = pages.all()
			page_ids = pages.values_list('id', flat=True)[1:]
			SitemapPages.objects.filter(id__in=page_ids).delete()
		return JsonResponse({'data': 'success', 'msg': 'Duplicated data successfully deleted!'})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': str(e)})



def checking_sitemap_lastmod_update(request, sitemap_page_id, sitemap_id, site_map, model_website):
	print('site url pages ni abot ko dri.')
	print(model_website)
	while True:
		try:
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
		except HttpError as error:
			page.status = 0
			page.save()
			# Handle the HttpError exception
			print(f'An HTTP error occurred: {error}')
			print(f'Status code: {error.resp.status}')
			print(f'Error content: {error.content}')
		except Exception as e:
			page.status = 0
			page.save()
		break
		time.sleep(3)
	return True


@login_required()
@csrf_exempt
def check_sitemap_lastmod_update(request):
	sitemap_page_id = request.POST.get('id')
	sitemap_id = request.POST.get('sitemap_id')
	site_map = Sitemap.objects.get(pk = sitemap_id)
	model_website = site_map.website
	threads = []
	if site_map:
		t = threading.Thread(target=checking_sitemap_lastmod_update, args=(request, sitemap_page_id, sitemap_id, site_map,
					model_website), daemon=True)
		t.start()
		threads.append(t)
		for thread in threads:
			thread.join()
	return JsonResponse({'data': 'success'})


@login_required
@csrf_exempt
def auto_check_siteurl_update_page(request, sitemap_page_id, sitemap_id):
	try:
		site_map = Sitemap.objects.get(pk = sitemap_id)
		page = SitemapPages.objects.get(pk = sitemap_page_id)
		domain = urlparse(page.pages).hostname
		print('domain', domain)
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
		print('You have successfully check the site url.......')
		# return JsonResponse({'data': 'success', 'msg': 'You have successfully check the site url.'})
	except HttpError as error:
		page.status = 0
		page.save()
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
		print(f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
										<b>Then How to Fix:</center></b><br> \
										<ul>\
											<li>Please activate the Google Search Console API + Google Index API</li>\
											<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
										</ul>')
		# return JsonResponse({'data': 'error', 'msg': f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
		# 								<b>Then How to Fix:</center></b><br> \
		# 								<ul>\
		# 									<li>Please activate the Google Search Console API + Google Index API</li>\
		# 									<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
		# 								</ul>'})
	except Exception as e:
		page.status = 0
		page.save()
		print("Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
						<b>Then How to Fix:</center></b><br> \
						<ul>\
							<li>Add Service Account To GSC as Owner</li>\
							<li>Please activate the Google Search Console API + Google Index API</li>\
							<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
						</ul>")
		# return JsonResponse({'data': 'error', 'msg': "Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
		# 				<b>Then How to Fix:</center></b><br> \
		# 				<ul>\
		# 					<li>Add Service Account To GSC as Owner</li>\
		# 					<li>Please activate the Google Search Console API + Google Index API</li>\
		# 					<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
		# 				</ul>"})


@login_required()
@csrf_exempt
def check_siteurl_update_page(request):
	sitemap_page_id = request.POST.get('id')
	sitemap_id = request.POST.get('sitemap_id')
	threads = []
	if sitemap_id:
		t = threading.Thread(target=auto_check_siteurl_update_page, args=(request, sitemap_page_id, sitemap_id), daemon=True)
		t.start()
		threads.append(t)
		for thread in threads:
			thread.join()
	return JsonResponse({'data': 'success'})




@login_required
@csrf_exempt
def auto_check_all_pages_siteurl_update_page(request, sitemap_page_id):
	try:
		print('sitemap_page_id', sitemap_page_id)
		site_map = Sitemap.objects.get(pk = sitemap_page_id)
		datas = SitemapPages.objects.filter(sitemap_id=sitemap_page_id)
		for page in datas:
			domain = urlparse(page.pages).hostname
			print('domain', domain)
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
			print('api key', site_map.apikey.indexApi)
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
			print('You have successfully check the site url.......')
	except HttpError as error:
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
		print(f'An HTTP error occurred with the status code: {error.resp.status} <br><br>' f'Error content: {error.content} <br><br><center>\
										<b>Then How to Fix:</center></b><br> \
										<ul>\
											<li>Please activate the Google Search Console API + Google Index API</li>\
											<li>Double Check API JSON <br> by checking you cant use this link: <a href="https://jsonlint.com/" target="_blank">https://jsonlint.com/</a></li>\
										</ul>')
	except Exception as e:
		print("Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
						<b>Then How to Fix:</center></b><br> \
						<ul>\
							<li>Add Service Account To GSC as Owner</li>\
							<li>Please activate the Google Search Console API + Google Index API</li>\
						<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
					</ul>")


@login_required()
@csrf_exempt
def check_all_pages_siteurl_update_page(request):
	sitemap_page_id = request.POST.get('pk')
	threads = []
	if sitemap_page_id:
		t = threading.Thread(target=auto_check_all_pages_siteurl_update_page, args=(request, sitemap_page_id), daemon=True)
		t.start()
		threads.append(t)
		for thread in threads:
			thread.join()
	return JsonResponse({'data': 'success'})


@csrf_exempt
def user_check_all_sitemap_gsc(request, pk):
	print(pk)
	idcheck = re.split(',', pk)
	print(idcheck)
	#Try Catch the error exeption of this method..	
	for row in idcheck:
		user_id = request.user.id
		site_map = Sitemap.objects.filter(id = row).first()
		print('site_map id', site_map.id)
		JSON_KEY_FILE = site_map.apikey.indexApi
		print(JSON_KEY_FILE)
		website_url = site_map.website

		#Check the domain of the webiste
		domain = urlparse(website_url).hostname
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
		site_map.clicks = rows[0]['clicks']
		site_map.impressions = rows[0]['impressions']
		site_map.ctr = rows[0]['ctr']
		site_map.positions = rows[0]['position']
		site_map.sitemap_status = 1
		site_map.save()
		log_history(user_id, 'successfully updating web pages for site {}.'.format(website_url))
	return JsonResponse({'data': 'success', 'msg': 'You have successfully adding web pages for sitemap.'})
	

#USER RANK TRACKER
@login_required
def user_rank_tracker(request):
	if request.method == 'POST':
		# try:
		with httpx.Client() as client:
			today = datetime.now().date()
			check_data = RankTracker.objects.filter(Q(keyword = request.POST.get('keyword')) & Q(date_created__date=today))
			if not check_data:
				if "'" not in request.POST.get('url'):
					myobj = {
						'keyword': request.POST.get('keyword'),
						'url': request.POST.get('url') if request.POST.get('url') else None,
						'location': request.POST.get('location') if request.POST.get('location') else 'Austin, Texas',
					}
					result = client.post("https://ranktracker.applikuapp.com/dataforseo/api/rank-tracker/", json=myobj,
											headers={'Content-Type': 'application/json',
													'Authorization': 'Token '
																		'e279b7682f87000aa8d3915702287ce6020a009e'},
											timeout=300)
					if result.status_code == 200 or result.status_code == 201:
						data = result.json()
						print('this is data', data)
						print('position', data[0]['position'])
						print('is_found', data[0]['is_found'])
						print('time_executed', data[0]['time_executed'])
						rank = RankTracker(
							keyword = request.POST.get('keyword'),
							url = request.POST.get('url'),
							location = request.POST.get('location') if request.POST.get('location') else 'Austin, Texas',
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
						rank = RankTracker(
							keyword = request.POST.get('keyword'),
							url = request.POST.get('url'),
							location = request.POST.get('location') if request.POST.get('location') else 'Austin, Texas',
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
						print("Something went wrong with the API")
					return JsonResponse({'data': 'success', 'msg': 'Pages successfully checking in rank tracker.'}, status=200)
				else:
					print('Skipping invalid URL')
					rank = RankTracker(
						keyword = request.POST.get('keyword'),
						url = request.POST.get('url'),
						location = request.POST.get('location') if request.POST.get('location') else 'Austin, Texas',
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
					return JsonResponse({'data': 'error', 'msg': 'Skipping invalid URL'})
			else:
				print('key word exist the same results today.')
				return JsonResponse({'data': 'success', 'msg': 'Websites successfully checking in rank tracker.'})
		# except Exception as e:
		# 	return JsonResponse({'data': 'error', 'msg': str(e)})
	context = {
		'active_tab': 'rank',
	}
	return render(request, 'indexer-user/user-rank-tracker.html', context)


@csrf_exempt
def user_update_rank_tracker(request, pk):
	print(pk)
	idcheck = re.split(',', pk)
	print(idcheck)
	for row in idcheck:
		check = RankTracker.objects.filter(Q(id=row)).first()
		print(check.id)
		with httpx.Client() as client:
			today = datetime.now().date()
			check_data = RankTracker.objects.filter(Q(user_id=request.user.id) & Q(id = check.id) & Q(keyword = check.keyword) & Q(date_created__date=today))
			if not check_data:
				myobj = {
					'keyword': check.keyword,
					'url': check.url,
					'location': check.location,
				}
				result = client.post("https://ranktracker.applikuapp.com/dataforseo/api/rank-tracker/", json=myobj,
						headers={'Content-Type': 'application/json',
								'Authorization': 'Token '
													'e279b7682f87000aa8d3915702287ce6020a009e'},
						timeout=300)
				if result.status_code == 200 or result.status_code == 201:
					data = result.json()
					print('this is data', data)
					print('position', data[0]['position'])
					print('is_found', data[0]['is_found'])
					print('time_executed', data[0]['time_executed'])
					RankTracker.objects.filter(id=check.id).update(
						rank_position = data[0]['position'],
						time_executed = data[0]['time_executed'],
						is_found = data[0]['is_found']
					)
					# CREATE AN HISTORY OF RANK TRACKER AND COST PER USED THE API
					check_rank_history = RankTrackerHistoryCost.objects.filter(Q(rank__user_id=request.user.id) & Q(rank_id = check.id) & Q(latest_rank_positions = data[0]['position']) & Q(date_updated__date=today))
					if not check_rank_history:
						RankTrackerHistoryCost.objects.create(
							rank_id = check.id,
							latest_rank_positions = data[0]['position'],
							cost = 0.000600,
							date_updated = datetime.now())
			else:
				print('is already today!')
	return JsonResponse({'data': 'success', 'msg': 'Websites successfully checking the updates in the rank tracker'})


#REGISTER USER
@login_required
@csrf_exempt
def register_user(request):
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
		req = requests.post("http://95.217.184.122/api/create-account/", json={'username':request.POST.get('username'), 'password':request.POST.get('password'),
						'email':request.POST.get('email')})
		print(req.text)
		req_token = requests.post("http://95.217.184.122/api/token/", json={'username':request.POST.get('username'), 
									  'password':request.POST.get('password')})
		print(req_token.text)
		ClientSettings.objects.create(
			user = user,
			access_token = req_token.json()['access']
		)
		return JsonResponse({'data': 'success', 'msg': 'You have successfully register the user.'})

	context = {
		'active_tab': 'reg_user',
	}
	return render(request, 'indexer-user/register_user.html', context)


@login_required
@csrf_exempt
def generate_client_toker_user(request):
	try:
		user = CustomUser.objects.get(pk = request.POST.get('id'))
		print('password', make_password(user.password))
		req = requests.post("http://95.217.184.122/api/create-account/", json={'username':user.username, 'password':user.password,
							'email':user.email})
		print(req.text)
		req_token = requests.post("http://95.217.184.122/api/token/", json={'username':user.username, 'password':user.password})
		print(req_token.text)
		ClientSettings.objects.create(
			user = user,
			access_token = req_token.json()['access']
		)
		return JsonResponse({'data': 'success', 'msg': 'You have successfully register the user.'})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': str(e)})


#VIEW USER
@login_required
@csrf_exempt
def view_users(request):
	context = {
		'active_tab': 'user_list',
	}
	return render(request, 'indexer-user/view-users.html', context)
