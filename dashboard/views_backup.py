from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
import httplib2
import tempfile
import json
from django.shortcuts import render, get_object_or_404
import pandas as pd
from indexer.models import *
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
from django.db.models import Q, Func, F, Value, CharField, Count
from django.conf import settings
from django.contrib.auth.decorators import login_required

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
		print("urlNotificationMetadata.latestUpdate.url: {}".format(response["urlNotificationMetadata"]["latestUpdate"]["url"]))
		print("urlNotificationMetadata.latestUpdate.type: {}".format(response["urlNotificationMetadata"]["latestUpdate"]["type"]))
		print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(response["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
		print('this is k ', k)
		with open(tmp.name, 'a') as f:
			f.write('\n' + ','.join(k))


def CheckIndexed(response, url):
	for count, i in enumerate(response['organic_results'], 1):
		if url == i['link']:
			return '{} {} - {}'.format(url,"Indexed at position", count)


# def CheckIsIndexed(response, url):
# 	for count, i in enumerate(response['organic_results'], 1):
# 		if url == i['link']:
# 			return '{} {} - {}\n'.format(url,"Indexed at position", count)


# def CheckIsNotIndexed(response, url):
# 	for count, i in enumerate(response['organic_results'], 1):
# 		if url != i['link']:
# 			return '{} - {}\n'.format(url," Not Indexed")


def is_json(myjson):
	try:
		json.loads(myjson)
	except ValueError as e:
		return False
	return True


@login_required
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
		'index_jan': IndexerPages.objects.filter(index_status=1, indexed_date__month=1, indexed_date__year=year).count(),
		'none_index_jan': IndexerPages.objects.filter(index_status=0, indexed_date__month=1, indexed_date__year=year).count(),

		'index_feb': IndexerPages.objects.filter(index_status=1, indexed_date__month=2, indexed_date__year=year).count(),
		'none_index_feb': IndexerPages.objects.filter(index_status=0, indexed_date__month=2, indexed_date__year=year).count(),

		'index_march': IndexerPages.objects.filter(index_status=1, indexed_date__month=3, indexed_date__year=year).count(),
		'none_index_march': IndexerPages.objects.filter(index_status=0, indexed_date__month=3, indexed_date__year=year).count(),

		'index_april': IndexerPages.objects.filter(index_status=1, indexed_date__month=4, indexed_date__year=year).count(),
		'none_index_april': IndexerPages.objects.filter(index_status=0, indexed_date__month=4, indexed_date__year=year).count(),

		'index_may': IndexerPages.objects.filter(index_status=1, indexed_date__month=5, indexed_date__year=year).count(),
		'none_index_may': IndexerPages.objects.filter(index_status=0, indexed_date__month=5, indexed_date__year=year).count(),

		'index_june': IndexerPages.objects.filter(index_status=1, indexed_date__month=6, indexed_date__year=year).count(),
		'none_index_june': IndexerPages.objects.filter(index_status=0, indexed_date__month=6, indexed_date__year=year).count(),

		'index_july': IndexerPages.objects.filter(index_status=1, indexed_date__month=7, indexed_date__year=year).count(),
		'none_index_july': IndexerPages.objects.filter(index_status=0, indexed_date__month=7, indexed_date__year=year).count(),

		'index_aug': IndexerPages.objects.filter(index_status=1, indexed_date__month=8, indexed_date__year=year).count(),
		'none_index_aug': IndexerPages.objects.filter(index_status=0, indexed_date__month=8, indexed_date__year=year).count(),

		'index_sep': IndexerPages.objects.filter(index_status=1, indexed_date__month=9, indexed_date__year=year).count(),
		'none_index_sep': IndexerPages.objects.filter(index_status=0, indexed_date__month=9, indexed_date__year=year).count(),

		'index_oct': IndexerPages.objects.filter(index_status=1, indexed_date__month=10, indexed_date__year=year).count(),
		'none_index_oct': IndexerPages.objects.filter(index_status=0, indexed_date__month=10, indexed_date__year=year).count(),

		'index_nov': IndexerPages.objects.filter(index_status=1, indexed_date__month=11, indexed_date__year=year).count(),
		'none_index_nov': IndexerPages.objects.filter(index_status=0, indexed_date__month=11, indexed_date__year=year).count(),

		'index_dec': IndexerPages.objects.filter(index_status=1, indexed_date__month=12, indexed_date__year=year).count(),
		'none_index_dec': IndexerPages.objects.filter(index_status=0, indexed_date__month=12, indexed_date__year=year).count(),	
	}
	return render(request, 'indexer-admin/dashboard.html', context)	


@login_required
def dashboard_index_page(request):
	if request.method == 'POST':
		if is_json(request.POST.get('keys')):
			check = IndexApi.objects.filter(email=request.POST.get('email'))
			if check:
				return JsonResponse({'data': 'error', 'msg': 'Email api already exist.'})
			else:
				index = IndexApi(
					user_id = request.user.id,
					email = strip_tags(request.POST.get('email')),
					indexApi = json.loads(request.POST.get('keys')),
					status = 1 if request.POST.get('status') else 0
				)
				index.save()
				log_history(request.user.id, 'added new api {}.'.format(request.POST.get('email')))
				return JsonResponse({'data': 'success', 'msg': 'You have successfully added new api keys.'})
		else:
			return JsonResponse({'data': 'error', 'msg': 'Invalid api keys.'})
	context = {
		'li': 'index_api'
	}		
	return render(request, 'indexer-admin/index-api.html', context)


@login_required
def index_api_update(request):
	if request.method == 'POST':
		if is_json(request.POST.get('index_index_api')):
			api_check = IndexApi.objects.filter(id=request.POST.get('pk')).first()
			check = IndexApi.objects.filter(Q(email=request.POST.get('index_email')) & ~Q(email=api_check.email))
			if check:
				return JsonResponse({'data': 'error', 'msg': 'Email api already exist.'})
			else:
				index = IndexApi.objects.filter(id=request.POST.get('pk')).update(
					email = strip_tags(request.POST.get('index_email')),
					indexApi = json.loads(request.POST.get('index_index_api')),
					status = 1 if request.POST.get('index_status') else 0
				)
				log_history(request.user.id, 'updating the api {}.'.format(request.POST.get('index_email')))
				return JsonResponse({'data': 'success', 'msg': 'You have successfully update the api keys.'})
		else:
			return JsonResponse({'data': 'error', 'msg': 'Invalid api keys.'})


@login_required
def dashboard_indexing_website(request):
	if request.method == 'POST':
		index = IndexApi.objects.filter(id=request.POST.get('api_email')).first()
		# website = Website.objects.filter(indexapi=index).first()
		url = request.POST.get('website')
		JSON_KEY_FILE = index.indexApi

		SCOPES = ["https://www.googleapis.com/auth/indexing"]
		ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
		INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

		# Authorize credentials
		credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
		http = credentials.authorize(httplib2.Http())
		service = build('indexing', 'v3', credentials=credentials)
		batch = service.new_batch_http_request(callback=insert_event)
		if request.POST.get('index_now'):
			global tmp
			tmp = tempfile.NamedTemporaryFile(delete=False)
			for url in request.POST.get('pages').split('\n'):
				batch.add(service.urlNotifications().publish(
					body={"url": url.rstrip(), "type": 'URL_UPDATED'}))
			batch.execute()
			k = ''
			web = ''
			with open(tmp.name) as f:
				for line in f:
					k += line
			web = Website(
				indexapi_id = request.POST.get('api_email'),
				website = request.POST.get('website'),
				pages = request.POST.get('pages'),
				times_indexed = 1,
				index_now = True,
				jsonFile = k,
			)
			web.save()
			with open(tmp.name) as f:
				index_page = []
				noneindex_page = []
				for line in f:
					pages = line.replace("\n","")
					if pages.split(",")[0] != '':
						print('this pages', pages.split(",")[0])
						print('this date', pages.split(",")[1])
						params = {
							"api_key": "ef484e7a9446d3485bc79b916828a4d9c9db9fda1cadf28b47db87a18f2877e2",
							"device": "desktop",
							"engine": "google",
							"q": pages.split(",")[0],
							"location": "Austin, Texas, United States",
							"google_domain": "google.com",
							"gl": "us",
							"hl": "en"
						}
						search = GoogleSearch(params)
						results = search.get_dict()
						status = CheckIndexed(results, pages.split(",")[0])
						index_pages = IndexerPages(
							web_id = web.id,
							url = pages.split(",")[0],
							indexed_date = pages.split(",")[1],
							index_status = 0 if status is None else 1
						)
						index_pages.save()
						print('this is status', status)
			tmp.close()
		else:
			web = Website(
				indexapi_id = request.POST.get('api_email'),
				website = request.POST.get('website'),
				pages = request.POST.get('pages'),
				times_indexed = 1,
				index_now = False,
			)
			web.save()
			log_history(request.user.id, 'indexing the website {}.'.format(request.POST.get('website')))
		return JsonResponse({'data': 'success', 'msg': 'You have successfully added new website indexing.'})
			 
	context = {
		'li': 'index_web',
		'index_api': IndexApi.objects.all()
	}		
	return render(request, 'indexer-admin/index-websites.html', context)


@login_required
def update_website_index(request, pk):
	if request.method == 'POST':
		if request.POST.get('check_index'):
			web = Website.objects.get(pk=pk)
			url = web.website
			JSON_KEY_FILE = web.indexapi.indexApi

			SCOPES = ["https://www.googleapis.com/auth/indexing"]
			ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
			INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"

			# Authorize credentials
			credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
			http = credentials.authorize(httplib2.Http())
			service = build('indexing', 'v3', credentials=credentials)
			batch = service.new_batch_http_request(callback=insert_event)
			
			indexYes = 0
			indexNo = 0
			status = ''
			isindex = ''
			isnotindex = ''
			isnotindext_text = ''
			isindext_text = ''
			restText = ''
			for url in web.pages.split('\n'):
				global tmp
				tmp = tempfile.NamedTemporaryFile(delete=False)
				batch.add(service.urlNotifications().publish(
					body={"url": url.rstrip(), "type": 'URL_UPDATED'}))
				k = ''
				with open(tmp.name) as f:
					for line in f:
						k += line
				url = url.rstrip().lstrip()
				params = {
					"api_key": "ef484e7a9446d3485bc79b916828a4d9c9db9fda1cadf28b47db87a18f2877e2",
					"device": "desktop",
					"engine": "google",
					"q": url,
					"location": "Austin, Texas, United States",
					"google_domain": "google.com",
					"gl": "us",
					"hl": "en"
				}
				search = GoogleSearch(params)
				results = search.get_dict()
				restText = CheckIndexed(results, url)
				check_again = CheckIndexed(results, url)
				check_perpage = IndexerPages.objects.filter(url=url)
				if not check_perpage:
					index_pages = IndexerPages(
						web_id = pk,
						url = url,
						indexed_date = timezone.now(),
						index_status = 0 if restText is None else 1
					)
					index_pages.save()

				print('this is status', status)
				if restText is None:
					restText = '{} - {}\n'.format(url, 'Indexed None')
					isnotindext_text = '{} - {}\n'.format(url, 'Indexed None')
					indexYes += 1
				else:
					isindext_text = '{} - {}\n'.format(url, 'Indexed Yes')
					indexNo += 1

				print('restText', restText)
				status += "{}, {}\n".format(timezone.now(),restText)
				isnotindex += isnotindext_text
				isindex += isindext_text
				print('isnotindex', isnotindex)

			check_is_right = IndexWebTracking.objects.filter(index_web_id = pk, is_right=1).first()
			update_tracking = IndexWebTracking(
				index_web_id = pk,
				updated_by_id = request.user.id,
				updated_at = timezone.now(),
				is_right = 0 if check_is_right else 1
			)
			update_tracking.save()
			web.jsonFile = '{} \n{}'.format(web.jsonFile, k) if web.jsonFile else k
			web.times_indexed = web.times_indexed + 1
			web.JsonResponse = status
			web.NonindexedPages = isnotindex
			if check_again:
				web.indexedPages = restText
			if not web.updated_at:
				web.updated_at = timezone.now()
			web.indexedRate = int((indexYes/(indexNo+indexYes))*100)
			web.check_index = True
			web.times_indexedRate = web.times_indexedRate + 1 if web.times_indexedRate else 1
			web.save()
			batch.execute()
			tmp.close()
			log_history(request.user.id, 'update indexing the website {}.'.format(web.website))
		return JsonResponse({'data': 'success', 'msg': 'You have successfully the indexing website.'})
	context = {
		'pk': pk,
		'web': Website.objects.get(pk=pk),
		'first_update': Website.objects.filter(id = pk).first(),
		'tracking': IndexWebTracking.objects.filter(index_web_id = pk).order_by('-updated_at'),
		'index_api': IndexApi.objects.all()
	}
	return render(request, 'indexer-admin/view_websites_index.html', context)


def get_url_shortner_api(request):
	result = requests.get('https://urlshortner.applikuapp.com/shorten/post/', headers={'Content-Type': 'application/json'})
	json_data = json.loads(result.text)
	return JsonResponse({'data': json_data})


@login_required
def dashboard_url_shortener(request):
	if request.method == 'POST':
			return JsonResponse({'data': 'success', 'msg': 'You have successfully added new api keys.'})
	context = {
		'li': 'url_short',
	}		
	return render(request, 'indexer-admin/url_shortener-api.html', context)


@login_required
def dashboard_log_history(request):
	context = {
		'li': 'settings',
	}		
	return render(request, 'indexer-admin/log_history.html', context)
