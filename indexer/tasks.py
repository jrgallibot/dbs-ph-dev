from celery import shared_task
import logging
from celery.utils.log import get_task_logger
from .models import *
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from apiclient.discovery import build
import json
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import pandas as pd
from mobile_friendly.models import MobileFriendlyPages, MobileFriendWeb
import httpx
import time
import asyncio
import threading
import os
from celery.exceptions import SoftTimeLimitExceeded
from open_ai.models import OpenAiContent, OpenAiKey, OpenAiContentResults
import openai

logger = get_task_logger('tasks')
start_time = time.time()

# Set configurations
key = OpenAiKey.objects.filter(id = 1, status=1).first()
engine = 'text-davinci-003'
temperature = 0.3
max_tokens = 2048
top_p = 0.3
frequency_penalty = 0
presence_penalty = 0

def GenerateCompletion(prompt):
	openai.api_key = key.api.strip()
	return openai.Completion.create(
		engine=engine,
		prompt=prompt,
		temperature=float(temperature),
		max_tokens=int(max_tokens),
		top_p=int(top_p),
		frequency_penalty=int(frequency_penalty),
		presence_penalty=int(presence_penalty)
	)


def GenerateOutline(headers):
	outline = 'Definition'
	for header in headers:
		outline = '{}\n{}'.format(outline, header)
	return outline


@shared_task(name='GenerateArticle')
def GenerateArticle(keyword: str):
	print(keyword)
	# Generate the headers
	headers_prompt = 'For a blog topic "{}", create a logically ordered list in JSON format, of 15 H2 items that ' \
		   'comprehensively cover the blog topic without using any of these words or their variations: {},' \
		   'Introduction, Conclusion, FAQs.'.format(keyword, keyword.replace(' ', ''))
	headers = json.loads(GenerateCompletion(headers_prompt)['choices'][0]['text'])
	headers = [x['h2'] for x in headers]
	print('this is headers', headers)

	# Initialize variable to store the contents of the articles
	article_content = []
	# Generate the introduction
	introduction_prompt = '"""Article Title: {}\n\nArticle Outline:\n{}"""\n\nWith pronouns and contractions, write ' \
						  'a 150-word introduction about the article above, using 3 paragraphs. Use personal ' \
						  'pronouns.'.format(keyword, GenerateOutline(headers))
	introduction = GenerateCompletion(introduction_prompt)['choices'][0]['text'].strip()
	article_content.append({'Introduction': introduction})
	print('this is introduction', introduction)

	# Generate section one
	section_one_prompt = '"""Article Title: {}\n\nFirst Topic: {}\n\nWrite the first section with pronouns, ' \
						 'contractions, and while following these rules: 1) Write the first section as only three ' \
						 'paragraphs, without conjunctive adverbs conjoining sentences. 2) In the last paragraph, ' \
						 'do not say "In conclusion" or "Finally". Proofread the first section.'\
		.format(keyword, headers[0])
	section_one = GenerateCompletion(section_one_prompt)['choices'][0]['text'].strip()
	article_content.append({headers[0]: section_one})
	print('this is section_one', section_one)

	# Generate remaining sections
	for i in range(1, len(headers)):
		section_prompt = '"""Article Title: {}\n\nPrevious Section Topic: {}\n\nSubsequent Section Topic: {}\n\n' \
						 'Start with a unique transition from the previous section and write the subsequent section, ' \
						 'with pronouns, contractions, and while following these rules: 1) Write the subsequent ' \
						 'section as only three paragraphs, without conjunctive adverbs conjoining sentences. ' \
						 '2) In the last paragraph, do not say "In conclusion" or "Finally". ' \
						 'Proofread subsequent section about {}.'\
			.format(keyword, headers[i - 1], headers[i], headers[i])
		section = GenerateCompletion(section_prompt)['choices'][0]['text'].strip()
		article_content.append({headers[i]: section})
		print('this is section', section)

	# Generate the conclusion
	conclusion_prompt = '"""Article Title: {}\n\nArticle Outline:\n{}"""\n\nWith pronouns and contractions, write a ' \
						'150-word conclusion about the article above, using 3 paragraphs. Use personal pronouns.' \
		.format(keyword, GenerateOutline(headers))
	conclusion = GenerateCompletion(conclusion_prompt)['choices'][0]['text'].strip()
	article_content.append({'Conclusion': conclusion})
	print('this is conclusion', conclusion)
	
	return article_content


@shared_task(name='checking_the_mobile_friendly')
def checking_the_mobile_friendly(web_id: int):
	print('helloooooooooooooo')
	while True:
		url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'
		global tmp
		tmp = tempfile.NamedTemporaryFile(delete=False)
		web = MobileFriendWeb.objects.get(pk = web_id)
		pages = MobileFriendlyPages.objects.filter(Q(web_id = web.id) & 
			~Q(status__icontains='MOBILE_FRIENDLY')
			& ~Q(url__isnull=True))
		if pages:
			for row in pages:
				print('pages ', row.url.rstrip())
				params = {
					'url': row.url.rstrip(),
					# 'requestScreenshot': 'true',
					'key': web.api.indexApi
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
						row.status = 'PAGE_UNREACHABLE'
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
			with open(tmp.name) as f:
				for line in f:
					k += line
			print('this is k', k)
			up_mobile = MobileFriendWeb.objects.get(pk = web.id)
			up_mobile.times_checked += 1
			up_mobile.result = k
			up_mobile.save()
			tmp.close()
	return True
	


@shared_task(name='per_day_update_index_rate')
def per_day_update_index_rate():
	print('per_day_update_index_rate')
	logger.info("The per_day_update_index_rate task just ran.")
	web = Website.objects.all()
	for w in web:
		url = w.website
		SCOPES = ["https://www.googleapis.com/auth/indexing"]
		ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

		# Authorize credentials
		credentials = ServiceAccountCredentials.from_json_keyfile_dict(w.indexapi.indexApi, scopes=SCOPES)
		http = credentials.authorize(httplib2.Http())
		service = build('indexing', 'v3', credentials=credentials)
		batch = service.new_batch_http_request(callback=insert_event2)

		pages = IndexerPages.objects.filter(Q(web_id=w.id) & Q(index_status__isnull=True)
												| Q(index_status=0)
												| Q(index_status=2))
		numsite_result = f'\n Updated {pages.count()} pages on {timezone.now()}'
		print(numsite_result)
		w.jsonFile += numsite_result
		w.updated_at = timezone.now()
		w.times_indexed += 1
		w.save()
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
					check_dt.updated_at = timezone.now()
					if not check_dt.indexed_date:
						check_dt.indexed_date = timezone.now()
					check_dt.date_tracking = "Last update: {}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
					check_dt.save()
				else:
					count_days = numOfDays(row.updated_at, datetime.today())
					print('this is count_days ', count_days)

					# Check if it is in 3 days above
					if not count_days > 6:
						print('check if it is not beyond in 3 days')
						# Check if it is index today
						if not now.strftime("%d/%m/%Y") == row.updated_at.strftime("%d/%m/%Y"):
							print('check if goes here')
							batch.add(service.urlNotifications().publish(
								body={"url": row.url.rstrip(), "type": 'URL_UPDATED'}))
							result_dt_tracking = "{}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
							upage = IndexerPages.objects.get(pk=row.id)
							upage.updated_at = timezone.now()
							if not upage.indexed_date:
								upage.indexed_date = timezone.now()
							upage.date_tracking = 'Last update: ' + upage.date_tracking + "\n" + result_dt_tracking if upage.date_tracking else 'Last update: ' + result_dt_tracking
							upage.save()
						else:
							pass
					else:
						pass

			# Check total usage of api
			today = datetime.now()
			up_usage = IndexerApiUsageTracking.objects.filter(api_id=w.indexapi_id,
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
					print('You have reached the maximum limit of API request for today')
			else:
				usage = IndexerApiUsageTracking(
					api_id=w.indexapi_id,
					total=len(data_arr),
					status=1
				)
				usage.save()
			batch.execute()
		except:
			w.jsonFile += f'\n Error Updating Indexer Automatically'
			w.save()
		else:
			pass


@shared_task(name='every_fourth_checking_index')
def every_fourth_checking_index():
	print('day 4 of checking in index....')
	logger.info("day 4 of checking in index....")
	web = Website.objects.values_list('id')
	pages = IndexerPages.objects.filter(Q(web_id__in=web) & Q(index_status__isnull=True)
										| Q(index_status=0)
										| Q(index_status=2))
	for row in pages:
		check_dt = IndexerPages.objects.filter(id=row.id, updated_at__isnull=True).first()
		if check_dt:
			check_dt.updated_at = timezone.now()
			if not check_dt.indexed_date:
				check_dt.indexed_date = timezone.now()
			check_dt.date_tracking = "Last update: {}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
			check_dt.save()
		else:
			count_days = numOfDays(row.updated_at, datetime.today())
			if not count_days > 6:
				print('this is count_days ', count_days)
			elif count_days == 7:
				if "'" not in row.url:
					myobj = {
						'keyword': f"{row.url}",
						'location': 'Austin, Texas',
					}
					print(myobj)
					result = requests.post("https://ranktracker.applikuapp.com/dataforseo/api/search/", json=myobj,
										   headers={'Content-Type': 'application/json',
													'Authorization': 'Token '
																	 'e279b7682f87000aa8d3915702287ce6020a009e'},
										   timeout=300)
					data = result.json()
					if result.status_code == 200 or result.status_code == 201:
						data = result.json()
						if data[0]['status_code'] == 20000:
							result = json.loads(data[0]['json_result'])
							organic = result['tasks'][0]['result'][0]['items']
							index_checker = False
							rank_absolute = None
							for i in organic:
								print(f"URLS: {row.url} vs {i['url']}")
								# url_parsed = urlparse(row['url']) used to parse string url
								# if url == str(url_parsed.netloc) or url == str(row['url']): To check if same domain
								url_1 = row.url
								url_1[-1].replace('/', '')

								url_2 = i['url']
								url_2[-1].replace('/', '')

								if url_1 == url_2:
									row.index_status = 1
									row.rank = i['rank_absolute']
									row.save()
									index_checker = True
									rank_absolute = i['rank_absolute']

							if index_checker:
								print(f"Url {row.url} Indexed with a rank of {rank_absolute}")
							else:
								# Incomplete Status Code = 0
								row.index_status = 0
								row.save()
								print(f"Url {row.url} not yet Indexed")
				else:
					# Invalid URL Status Code = 2
					row.index_status = 2
					row.save()
					print('Skipping invalid URL')


@shared_task(name="update_index_rate")
def update_index_rate(model_id: int):
	print('hello')
	web = Website.objects.get(pk=model_id)
	url = web.website
	JSON_KEY_FILE = web.indexapi.indexApi
	pages = IndexerPages.objects.filter(Q(web_id=model_id))

	SCOPES = ["https://www.googleapis.com/auth/indexing"]
	ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

	# Authorize credentials
	credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
	http = credentials.authorize(httplib2.Http())
	service = build('indexing', 'v3', credentials=credentials)
	batch = service.new_batch_http_request(callback=insert_event2)
	numsite = ''
	numsite_result = ''
	# try:
	now = datetime.now()
	for row in pages:
		check_dt = IndexerPages.objects.filter(id=row.id, updated_at__isnull=True).first()
		if check_dt:
			print('check_dt')
			batch.add(service.urlNotifications().publish(
				body={"url": row.url.rstrip(), "type": 'URL_UPDATED'}))
			check_dt.updated_at = timezone.now()
			if not check_dt.indexed_date:
				check_dt.indexed_date = timezone.now()
			check_dt.date_tracking = "Last update: {}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
			check_dt.save()
		else:
			count_days = numOfDays(row.updated_at, datetime.today())
			print('this is count_days ', count_days)

			# Check if it is in 3 days above
			if not count_days > 3:
				print('check if it is not beyond in 3 days')
				# Check if it is index today
				if not now.strftime("%d/%m/%Y") == row.updated_at.strftime("%d/%m/%Y"):
					print('check if goes here')
					batch.add(service.urlNotifications().publish(
						body={"url": row.url.rstrip(), "type": 'URL_UPDATED'}))
					result_dt_tracking = "{}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
					upage = IndexerPages.objects.get(pk=row.id)
					upage.updated_at = timezone.now()
					if not upage.indexed_date:
						upage.indexed_date = timezone.now()
					upage.date_tracking = 'Last update: ' + upage.date_tracking + "\n" + result_dt_tracking if upage.date_tracking else 'Last update: ' + result_dt_tracking
					upage.save()
				else:
					pass

			# Check the index result after 4 days in process of indexing
			elif count_days == 4:
				print('day 4 of checking in index....')
				myobj = {
					'keyword': row.url,
					'location': 'Austin, Texas',
				}
				if row.index_status != 1:
					if "'" not in row.url:
						result = requests.post("https://ranktracker.applikuapp.com/dataforseo/api/search/", json=myobj,
											   headers={'Content-Type': 'application/json',
														'Authorization': 'Token '
																		 'e279b7682f87000aa8d3915702287ce6020a009e'})
						if result.status_code == 200 or result.status_code == 201:
							data = result.json()
							if data[0]['status_code'] == 20000:
								result = json.loads(data[0]['json_result'])
								organic = result['tasks'][0]['result'][0]['items']
								index_checker = False
								rank_absolute = None
								for i in organic:
									print(f"URLS: {row.url} vs {i['url']}")
									url_1 = row.url
									url_1[-1].replace('/', '')

									url_2 = i['url']
									url_2[-1].replace('/', '')

									if url_1 == url_2:
										row.index_status = 1
										row.rank = i['rank_absolute']
										row.save()
										index_checker = True
										rank_absolute = i['rank_absolute']

								if index_checker:
									print(f"Url {row.url} Indexed with a rank of {rank_absolute}")
								else:
									# Incomplete Status Code = 0
									row.index_status = 0
									row.save()
									print(f"Url {row.url} not yet Indexed")
						else:
							return JsonResponse(
								{'data': 'error', 'msg': 'Something went wrong with the API Service...'})
					else:
						# Invalid URL Status Code = 2
						row.index_status = 2
						row.updated_at = timezone.now()
						row.save()
						print('Skipping invalid URL')
			else:
				pass
	batch.execute()
	numsite_result = f'\n Updated {pages.count()} pages on {timezone.now()}'
	web.jsonFile += numsite_result
	web.updated_at = timezone.now()
	web.times_indexed += 1
	web.save()


# except:
# 	web.jsonFile += f'\n Error Updating Indexer Automatically'
# 	web.save()
# else:
# 	pass


@shared_task(name="update_sitemap_task")
def update_sitemap_task(model_id: int):
	# model_instance = Sitemap()
	model_instance = Sitemap.objects.get(pk=model_id)
	model_website = model_instance.website
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
	results = "<table><tr><th>Url</th><th>Date</th></tr>"
	for i in pag2:
		results += f" <tr>    <td>{i[0]}</td>    <td>{i[1]}</td>  </tr>"
	for i in nonepages:
		print(i[1])
		results += f" <tr>    <td>{i[0]}</td>    <td>{i[1]}</td>  </tr>"

	results += '</table>'
	model_instance.results = results
	model_instance.website = model_website
	model_instance.save()


@shared_task(name="auto_run_indexer")
def auto_run_indexer():
	print('hi')
	website_instances = Website.objects.filter(times_indexed__lte=5).exclude(pages__exact='')
	for model_instance in website_instances:
		if len(model_instance.pages.split('\n')) > 2:
			try:
				if ((timezone.now() - model_instance.updated_at).days > 1) & (
						len(model_instance.pages.split('\n')) > 1):
					url = model_instance.website

					SCOPES = ["https://www.googleapis.com/auth/indexing"]
					ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

					# Authorize credentials
					credentials = ServiceAccountCredentials.from_json_keyfile_dict(model_instance.indexapi.indexApi,
																				   scopes=SCOPES)
					http = credentials.authorize(httplib2.Http())
					service = build('indexing', 'v3', credentials=credentials)
					batch = service.new_batch_http_request(callback=insert_event2)
					for url in model_instance.pages.split('\n'):
						batch.add(service.urlNotifications().publish(
							body={"url": url.rstrip(), "type": 'URL_UPDATED'}))
					batch.execute()
					numsite = len(model_instance.pages.split('\n'))
					model_instance.jsonFile += f'\n Updated {numsite} pages on {timezone.now()}'
					model_instance.updated_at = timezone.now()
					model_instance.times_indexed += 1
					model_instance.save()
				else:
					pass
			except:
				model_instance.jsonFile += f'\n Error Updating Indexer Automatically'
				model_instance.times_indexed = 404
				model_instance.save()
			else:
				pass


@shared_task(name="auto_run_indexer_repeater")
def auto_run_indexer_repeater():
	with transaction.atomic():
		website_instances = Website.objects.filter(times_indexed__gte=99)
		for model_instance in website_instances:
			url = model_instance.website

			SCOPES = ["https://www.googleapis.com/auth/indexing"]
			ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

			# Authorize credentials
			credentials = ServiceAccountCredentials.from_json_keyfile_dict(model_instance.indexapi.indexApi,
																		   scopes=SCOPES)
			http = credentials.authorize(httplib2.Http())
			service = build('indexing', 'v3', credentials=credentials)
			batch = service.new_batch_http_request(callback=insert_event2)
			for url in model_instance.pages.split('\n'):
				batch.add(service.urlNotifications().publish(
					body={"url": url.rstrip(), "type": 'URL_UPDATED'}))
			batch.execute()
			numsite = len(model_instance.pages.split('\n'))
			model_instance.jsonFile += f'\n Updated {numsite} pages on {timezone.now()}'
			model_instance.updated_at = timezone.now()
			model_instance.times_indexed += 1
			model_instance.save()


@shared_task(name="run_indexer_5")
def run_indexer_5():
	website_instances = Website.objects.filter(RunIndexer5=True).exclude(pages__exact='')
	for model_instance in website_instances:
		if len(model_instance.pages.split('\n')) > 2:
			try:
				if ((timezone.now() - model_instance.updated_at).days > 2) & (
						len(model_instance.pages.split('\n')) > 1):
					url = model_instance.website

					SCOPES = ["https://www.googleapis.com/auth/indexing"]
					ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

					# Authorize credentials
					credentials = ServiceAccountCredentials.from_json_keyfile_dict(model_instance.indexapi.indexApi,
																				   scopes=SCOPES)
					http = credentials.authorize(httplib2.Http())
					service = build('indexing', 'v3', credentials=credentials)
					batch = service.new_batch_http_request(callback=insert_event2)
					for url in model_instance.pages.split('\n'):
						batch.add(service.urlNotifications().publish(
							body={"url": url.rstrip(), "type": 'URL_UPDATED'}))
					batch.execute()
					numsite = len(model_instance.pages.split('\n'))
					model_instance.jsonFile += f'\n Updated {numsite} pages on {timezone.now()}'
					model_instance.updated_at = timezone.now()
					model_instance.times_indexed += 1
					if (model_instance.times_indexed % 5 == 0):
						model_instance.RunIndexer5 = False
					model_instance.save()
				else:
					pass
			except:
				model_instance.jsonFile += f'\n Error Updating Indexer Automatically'
				model_instance.times_indexed = 404
				model_instance.RunIndexer5 = False
				model_instance.save()
			else:
				pass
