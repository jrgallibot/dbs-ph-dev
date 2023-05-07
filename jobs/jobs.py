from django.conf import settings
import json
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import httplib2
import pandas as pd
from urllib.parse import urlparse
from django.shortcuts import render
import requests
import base64
from indexer.models import IndexApi, insert_event2, numOfDays
from dashboard.views import log_history
from asgiref.sync import async_to_sync, sync_to_async
from mobile_friendly.models import MobileFriendWeb, MobileFriendlyPages
from indexer.models import Website, IndexerPages, IndexerApiUsageTracking, Sitemap, SitemapPages, SitemapModUpdate
from django.utils import timezone
import tempfile
import random
from django.core.files.storage import FileSystemStorage
import socket
import httpx
import time
import asyncio
import threading
import os
from django.db.models import Q
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
from open_ai.models import OpenAiContent, OpenAiKey, OpenAiContentResults, OpenAiAssistedGC, OpenAiAssistedGCHeaders, OpenAiAssistedGCResults, OpenAiPrompt, \
	OpenAiCGPrompt, OpenAiPromptSubParent
import openai
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
start_time = time.time()
# Set configurations
key = OpenAiKey.objects.filter(id = 1, status=1).first()
engine = 'text-davinci-003'
max_tokens = 3863
temperature = 0.3
top_p = 0.3
frequency_penalty = 0
presence_penalty = 0

def GenerateCompletion(prompt):
	openai.api_key = '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'
	print('api key', openai.api_key)
	return openai.Completion.create(
		engine=engine,
		prompt=prompt,
		temperature=float(temperature),
		max_tokens=max_tokens,
		top_p=int(top_p),
		frequency_penalty=int(frequency_penalty),
		presence_penalty=int(presence_penalty)
	)


def GenerateOutline(headers):
	outline = 'Definition'
	for header in headers:
		outline = '{}\n{}'.format(outline, header)
	return outline

# SCHEDULE OPENAI
def SchedGenerateFirstSectionAndOtherSections():
	try:
		keyword = OpenAiAssistedGC.objects.filter(Q(is_cg=1) & Q(cg_status='Generating'))
		if keyword:
			print('naay cg')
			for row in keyword:
				#Initiate variables
				keyword = row.title
				pk = row.id
				prompt_id = row.prompt.id

				print('this is ', keyword, pk, prompt_id)

				print('this is prompt', prompt_id)

				headers_prompt = 'For a blog topic "{}", create a logically ordered list in JSON format, of 15 H2 items that ' \
					'comprehensively cover the blog topic without using any of these words or their variations: {},' \
					'Introduction, Conclusion, FAQs.'.format(keyword, keyword.replace(' ', ''))
				headers = json.loads(GenerateCompletion(headers_prompt)['choices'][0]['text'])
				for x in headers:
					print('headers', x['h2'])
					check_page = OpenAiAssistedGCHeaders.objects.filter(Q(ass_id=pk) & Q(headers=x['h2'].rstrip()))
					if check_page:
						print('duplicate found...')
						pass
					else:
						if not check_page:
							OpenAiAssistedGCHeaders.objects.create(
								ass_id=pk,
								headers=x['h2'],
								status='Pending'
							)
				all_data = OpenAiAssistedGCHeaders.objects.filter(Q(ass_id=pk) & Q(status='Pending')).all().order_by('id')
				if all_data:
					headers = [x.id for x in all_data]
					print(headers[0])

					sub_parent_prompt = OpenAiPromptSubParent.objects.filter(parent_id=prompt_id).order_by('prompt_id')
					for pr in sub_parent_prompt:
						print(pr.prompt_id)
						# Generate the introduction
						if pr.prompt_id == 1:
							print('1')
							chk_id = OpenAiAssistedGCHeaders.objects.filter(id = headers[0]).first()
							prompt_intro = OpenAiPrompt.objects.filter(id = 1).first()
							data_intro = prompt_intro.prompt
							prompt_intros = data_intro.replace('#KEYWORD', keyword).replace('#HEADER', GenerateOutline(headers))
							introduction = GenerateCompletion(prompt_intros)['choices'][0]['text'].strip()
							article_content = []
							article_content.append({'Introduction': introduction})
							chck_fst = OpenAiAssistedGCResults.objects.filter(results = article_content)
							if not chck_fst:
								OpenAiAssistedGCResults.objects.create(
									name = 'Introduction',
									results = article_content,
									order_by = 1,
									headers_id = chk_id.id
								)
							print('this is introduction', introduction)

						# Generate section one
						if pr.prompt_id == 2:
							print('2')
							chk_id = OpenAiAssistedGCHeaders.objects.filter(id = headers[0]).first()
							prompt_section_one = OpenAiPrompt.objects.filter(id = 2).first()
							data_first = prompt_section_one.prompt
							print('data_first')
							prompt_one_section = data_first.replace('#KEYWORD', keyword).replace('#HEADER', chk_id.headers)
							print('prompt_one_section', prompt_one_section)
							section_one = GenerateCompletion(prompt_one_section)['choices'][0]['text'].strip()
							article_content = []
							article_content.append({chk_id.headers: section_one})
							chck_fst = OpenAiAssistedGCResults.objects.filter(results = article_content)
							if not chck_fst:
								OpenAiAssistedGCResults.objects.create(
									name = 'First Section',
									results = article_content,
									order_by = 2,
									headers_id = chk_id.id
								)
							chk_id.status = 'Done'
							chk_id.save()
							print('this is section_one', section_one)


						# Generate remaining sections
						if pr.prompt_id == 3:
							print('3')
							for i in range(1, len(headers)):
								chk_sec_id = OpenAiAssistedGCHeaders.objects.filter(id = headers[i]).first()
								chk_prev = OpenAiAssistedGCHeaders.objects.filter(id = headers[i - 1]).first()
								print('chk_prev.headers', chk_prev.headers)
								second_prompt = OpenAiPrompt.objects.filter(id=3).first()
								if second_prompt:
									data_two = second_prompt.prompt
									prompt_other_section = data_two.replace('#KEYWORD', keyword).replace('#PREV_HEADER', chk_prev.headers).replace('#HEADER', chk_sec_id.headers)
									section = GenerateCompletion(prompt_other_section)['choices'][0]['text'].strip()
									article_content = []
									article_content.append({chk_sec_id.headers: section})
									chck = OpenAiAssistedGCResults.objects.filter(results = article_content)
									if not chck:
										OpenAiAssistedGCResults.objects.create(
											name = 'Other Section',
											results = article_content,
											order_by = 3,
											headers_id = chk_sec_id.id
										)
									chk_sec_id.status = 'Done'
									chk_sec_id.save()
									print('this is section', section)

						# Generate the conclusion
						if pr.prompt_id == 4:
							print('4')
							chk_id = OpenAiAssistedGCHeaders.objects.filter(id = headers[0]).first()
							con_prompt = OpenAiPrompt.objects.filter(id=4).first()
							if con_prompt:
								data_con = con_prompt.prompt
								prompt_con = data_con.replace('#KEYWORD', keyword).replace('#HEADER', GenerateOutline(headers))
								conclusion = GenerateCompletion(prompt_con)['choices'][0]['text'].strip()
								article_content = []
								article_content.append({'Conclusion': conclusion})
								chck = OpenAiAssistedGCResults.objects.filter(results = article_content)
								if not chck:
									OpenAiAssistedGCResults.objects.create(
										name = 'Conclusion',
										results = article_content,
										order_by = 4,
										headers_id = chk_id.id
									)
								print('this is conclusion', conclusion)
					row.cg_status = 'Done'
					row.save()
				else:
					print('no data found in headers...')
				break
		else:
			print('No generating to execute')
	except requests.exceptions.HTTPError as err:
		print(f'An HTTP error occurred: {err}')
	except HttpError as error:
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
	except Exception as e:
		print(f'An HTTP error occurred: {e}')


def GenerateAssistedGCSchedule():
	try:
		keyword = OpenAiAssistedGC.objects.filter(~Q(is_cg=1) & Q(cg_status='Generating'))
		if keyword:
			print('naay assisted.')
			for row in keyword:
				#Initiate variables
				keyword = row.title
				pk = row.id
				prompt_id = row.prompt.id
				print('this is ', keyword, pk, prompt_id)
				print('this is prompt', prompt_id)
				all_data = OpenAiAssistedGCHeaders.objects.filter(Q(ass_id=pk) & Q(status='Pending')).all().order_by('id')
				if all_data:
					headers = [x.id for x in all_data]
					print('headers', headers[0])

					sub_parent_prompt = OpenAiPromptSubParent.objects.filter(parent_id=prompt_id).order_by('prompt_id')
					for pr in sub_parent_prompt:
						print(pr.prompt_id)
						# Generate the introduction
						if pr.prompt_id == 1:
							print('1')
							chk_id = OpenAiAssistedGCHeaders.objects.filter(id = headers[0]).first()
							prompt_intro = OpenAiPrompt.objects.filter(id = 1).first()
							data_intro = prompt_intro.prompt
							prompt_intros = data_intro.replace('#KEYWORD', keyword).replace('#HEADER', GenerateOutline(headers))
							introduction = GenerateCompletion(prompt_intros)['choices'][0]['text'].strip()
							article_content = []
							article_content.append({'Introduction': introduction})
							chck_fst = OpenAiAssistedGCResults.objects.filter(results = article_content)
							if not chck_fst:
								OpenAiAssistedGCResults.objects.create(
									name = 'Introduction',
									results = article_content,
									order_by = 1,
									headers_id = chk_id.id
								)
							print('this is introduction', introduction)

						# Generate section one
						if pr.prompt_id == 2:
							print('2')
							chk_id = OpenAiAssistedGCHeaders.objects.filter(id = headers[0]).first()
							prompt_section_one = OpenAiPrompt.objects.filter(id = 2).first()
							data_first = prompt_section_one.prompt
							print('data_first')
							prompt_one_section = data_first.replace('#KEYWORD', keyword).replace('#HEADER', chk_id.headers)
							print('prompt_one_section', prompt_one_section)
							section_one = GenerateCompletion(prompt_one_section)['choices'][0]['text'].strip()
							article_content = []
							article_content.append({chk_id.headers: section_one})
							chck_fst = OpenAiAssistedGCResults.objects.filter(results = article_content)
							if not chck_fst:
								OpenAiAssistedGCResults.objects.create(
									name = 'First Section',
									results = article_content,
									order_by = 2,
									headers_id = chk_id.id
								)
							chk_id.status = 'Done'
							chk_id.save()
							print('this is section_one', section_one)


						# Generate remaining sections
						if pr.prompt_id == 3:
							print('3')
							for i in range(1, len(headers)):
								chk_sec_id = OpenAiAssistedGCHeaders.objects.filter(id = headers[i]).first()
								chk_prev = OpenAiAssistedGCHeaders.objects.filter(id = headers[i - 1]).first()
								print('chk_prev.headers', chk_prev.headers)
								second_prompt = OpenAiPrompt.objects.filter(id=3).first()
								if second_prompt:
									data_two = second_prompt.prompt
									prompt_other_section = data_two.replace('#KEYWORD', keyword).replace('#PREV_HEADER', chk_prev.headers).replace('#HEADER', chk_sec_id.headers)
									section = GenerateCompletion(prompt_other_section)['choices'][0]['text'].strip()
									article_content = []
									article_content.append({chk_sec_id.headers: section})
									chck = OpenAiAssistedGCResults.objects.filter(results = article_content)
									if not chck:
										OpenAiAssistedGCResults.objects.create(
											name = 'Other Section',
											results = article_content,
											order_by = 3,
											headers_id = chk_sec_id.id
										)
									chk_sec_id.status = 'Done'
									chk_sec_id.save()
									print('this is section', section)

						# Generate the conclusion
						if pr.prompt_id == 4:
							print('4')
							chk_id = OpenAiAssistedGCHeaders.objects.filter(id = headers[0]).first()
							con_prompt = OpenAiPrompt.objects.filter(id=4).first()
							if con_prompt:
								data_con = con_prompt.prompt
								prompt_con = data_con.replace('#KEYWORD', keyword).replace('#HEADER', GenerateOutline(headers))
								conclusion = GenerateCompletion(prompt_con)['choices'][0]['text'].strip()
								article_content = []
								article_content.append({'Conclusion': conclusion})
								chck = OpenAiAssistedGCResults.objects.filter(results = article_content)
								if not chck:
									OpenAiAssistedGCResults.objects.create(
										name = 'Conclusion',
										results = article_content,
										order_by = 4,
										headers_id = chk_id.id
									)
								print('this is conclusion', conclusion)
				else:
					print('no data found in headers...')
		else:
			print('No generating to execute')
	except requests.exceptions.HTTPError as err:
		print(f'An HTTP error occurred: {err}')
	except HttpError as error:
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
	except Exception as e:
		print(f'An HTTP error occurred: {e}')

def GenerateArticleSchedule():
	data = OpenAiCGPrompt.objects.filter(cg__status='Generating').all()
	try:
		if data:
			for row in data:
				content = OpenAiContent.objects.filter(id = row.cg_id).first()
				# Generate the headers
				print(content.keyword)
				headers_prompt = 'For a blog topic "{}", create a logically ordered list in JSON format, of 15 H2 items that ' \
					'comprehensively cover the blog topic without using any of these words or their variations: {},' \
					'Introduction, Conclusion, FAQs.'.format(content.keyword, content.keyword.replace(' ', ''))
				headers_data = json.loads(GenerateCompletion(headers_prompt)['choices'][0]['text'])
				headers = [x['h2'] for x in headers_data]
				print('this is headers', headers)

				# Initialize variable to store the contents of the articles
				article_content = []
				sub_parent_prompt = OpenAiPromptSubParent.objects.filter(parent_id=row.prompt.id).order_by('prompt_id')
				for pr in sub_parent_prompt:
					print(pr.prompt_id)
					# Generate the introduction
					if pr.prompt_id == 1:
						prompt_intro = OpenAiPrompt.objects.filter(id = 1).first()
						data_intro = prompt_intro.prompt
						prompt_intro = data_intro.replace('#KEYWORD', content.keyword).replace('#HEADER', GenerateOutline(headers))
						introduction = GenerateCompletion(prompt_intro)['choices'][0]['text'].strip()
						article_content.append({'Introduction': introduction})
						print('this is introduction', introduction)

					# Generate section one
					if pr.prompt_id == 2:
						prompt_section_one = OpenAiPrompt.objects.filter(id = 2).first()
						data_first = prompt_section_one.prompt
						prompt_one_section = data_first.replace('#KEYWORD', content.keyword).replace('#HEADER', headers[0])
						section_one = GenerateCompletion(prompt_one_section)['choices'][0]['text'].strip()
						article_content.append({headers[0]: section_one})
						print('this is section_one', section_one)

					# Generate remaining sections
					if pr.prompt_id == 3:
						for i in range(1, len(headers)):
							second_prompt = OpenAiPrompt.objects.filter(id=3).first()
							if second_prompt:
								data_two = second_prompt.prompt
								prompt_other_section = data_two.replace('#KEYWORD', content.keyword).replace('#PREV_HEADER', headers[i - 1]).replace('#HEADER', headers[i])
								section = GenerateCompletion(prompt_other_section)['choices'][0]['text'].strip()
								article_content.append({headers[i]: section})
								print('this is section', section)

					# Generate the conclusion
					if pr.prompt_id == 4:
						con_prompt = OpenAiPrompt.objects.filter(id=4).first()
						if con_prompt:
							data_con = con_prompt.prompt
							prompt_con = data_con.replace('#KEYWORD', content.keyword).replace('#HEADER', GenerateOutline(headers))
							conclusion = GenerateCompletion(prompt_con)['choices'][0]['text'].strip()
							article_content.append({'Conclusion': conclusion})
							print('this is conclusion', conclusion)

				content.results = article_content
				content.status = 'Done'
				content.save()
				return article_content			
		else:
			print('no data in openai to generate...')
	except requests.exceptions.HTTPError as err:
		print(err)
	except HttpError as error:
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
	except Exception as e:
		print(e)

#SCHEDULE THE CHECK SITE URL UPDATE PAGES
def schedule_check_siteurl_update_page():
	try:
		print('hereeeee i goooo...')
		site_map = Sitemap.objects.all()
		for row in site_map:
			JSON_KEY = row.apikey.indexApi
			data_page = SitemapPages.objects.filter(sitemap_id=row.id, status=0)
			if data_page:
				for page in data_page:
					domain = urlparse( page.pages).hostname
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
						temp_file.write(json.dumps(JSON_KEY).encode('utf-8'))
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
			else:
				print('no data found......')
	except HttpError as error:
		site_map = Sitemap.objects.all()
		for row in site_map:
			page = SitemapPages.objects.filter(sitemap_id=row.id)
			for data in page:
				data.status = 0
				data.save()
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
		site_map = Sitemap.objects.all()
		for row in site_map:
			page = SitemapPages.objects.filter(sitemap_id=row.id)
			for data in page:
				data.status = 0
				data.save()
		print("Theres an error of decoding JSON in your API KEY: "+ str(e)+ "<br><br><center>\
						<b>Then How to Fix:</center></b><br> \
						<ul>\
							<li>Add Service Account To GSC as Owner</li>\
							<li>Please activate the Google Search Console API + Google Index API</li>\
							<li>Double Check API JSON <br> by checking you cant use this link: <a href='https://jsonlint.com/' target='_blank'>https://jsonlint.com/</a></li>\
						</ul>")

# SCHEDULE TO DELETE EMPTY PAGES IN WEBSITE
def empty_url_delete():
	pages = IndexerPages.objects.filter(Q(url__isnull=True) | Q(url="")).all()
	if pages:
		for row in pages:
			print(row.id)
			IndexerPages.objects.filter(id = row.id).delete()
	else:
		print('no url empty found..')


#SCHEDULE SITEMAP UPDATE DAILY
def schedule_sitemap_lastmod_update():
	site_map = Sitemap.objects.all()
	for row in site_map:
		model_website = row.website
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
			sitemap_page = SitemapPages.objects.filter(sitemap_id = row.id)
			for sitemap in sitemap_page:
				# Check if lastmod already exist with same value
				check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = sitemap.id)
				if not check_lastmod_exist:
					SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = sitemap.id, updated_at = datetime.now().date())
		for i in nonepages:
			sitemap_page = SitemapPages.objects.filter(sitemap_id = row.id)
			for sitemap in sitemap_page:
				# Check if lastmod already exist with same value
				check_lastmod_exist = SitemapModUpdate.objects.filter(last_mod = i[1], sitemap_page_id = sitemap.id)
				if not check_lastmod_exist:
					SitemapModUpdate.objects.create(last_mod = i[1], sitemap_page_id = sitemap.id, updated_at = datetime.now().date())
	print('success!')
	return True


#SCHEDULE MOBILE FRIENDLY
async def get_mobile_friendly_api(web):
	async with httpx.AsyncClient() as client:
		strings = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!"
		rand_string = ("".join(random.sample(strings, 6)))

		url = 'https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run'
		global tmp
		tmp = tempfile.NamedTemporaryFile(delete=False)
		now = datetime.now()
		for web_instance in web:
			api_key = web_instance.api.indexApi
			print(api_key)
			pages = MobileFriendlyPages.objects.filter(Q(web_id=web_instance.id) 
				& ~Q(status__icontains='MOBILE_FRIENDLY')
				& ~Q(url__isnull=True))
			if pages:
				for page_instance in pages:
					print('pages ', page_instance.url.rstrip())
					if page_instance.updated_at:
						print('dli ni null')
						count_days = numOfDays(page_instance.updated_at, datetime.today())
						if not count_days > 6:
							print('this is count_days ', count_days)
							print('check if it is not beyond in 6 days')
							# Check if it is mobile friendly today
							if not now.strftime("%d/%m/%Y") == page_instance.updated_at.strftime("%d/%m/%Y"):
								track_text = f'\n Last Update {timezone.now()}'
								page_instance.date_tracking += track_text
								page_instance.save()
								params = {
									'url': page_instance.url.rstrip(), 
									'requestScreenshot': 'true', 
									'key': api_key
								}
								x = await client.post(url, params=params, timeout=60)
								data = x.json()
								print(x.status_code)
								if x.status_code == 200 or x.status_code == 201:
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

										page_instance.status = data["mobileFriendliness"]
										page_instance.seconds = time.time() - start_time
										page_instance.results = data_results
										# page_instance.request_screenshot = 'mobile_friendly/{}.png'.format(rand_string)
										page_instance.save()
										print("--- %s seconds ---" % (time.time() - start_time))
									else:
										page_instance.results = None
										# page_instance.status = 'PAGE_UNREACHABLE'
										page_instance.status = 'NOT_MOBILE_FRIENDLY'
										page_instance.seconds = time.time() - start_time
										# row.request_screenshot = None
										page_instance.save()
										print("--- %s seconds ---" % (time.time() - start_time))

									#Generate results
									with open(tmp.name, 'a') as f:
										f.write('\n Page {}, status {} on {}'.format(page_instance.url.replace('\r',''),
													data["testStatus"]["status"],
													timezone.now()))
								else:
									print("Something went wrong with the API")
							else:
								print('oppppps naa nay na update krn.')
					else:
						print('null ni')
						page_instance.updated_at = timezone.now()
						page_instance.date_tracking = "Last update: {}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
						page_instance.save()
						params = {
							'url': page_instance.url.rstrip(), 
							'requestScreenshot': 'true', 
							'key': api_key
						}
						x = await client.post(url, params=params, timeout=60)
						data = x.json()
						print(x.status_code)
						if x.status_code == 200 or x.status_code == 201:
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

								page_instance.status = data["mobileFriendliness"]
								page_instance.seconds = time.time() - start_time
								page_instance.results = data_results
								# page_instance.request_screenshot = 'mobile_friendly/{}.png'.format(rand_string)
								page_instance.save()
								print("--- %s seconds ---" % (time.time() - start_time))
							else:
								page_instance.results = None
								# page_instance.status = 'PAGE_UNREACHABLE'
								page_instance.status = 'NOT_MOBILE_FRIENDLY'
								page_instance.seconds = time.time() - start_time
								# row.request_screenshot = None
								page_instance.save()
								print("--- %s seconds ---" % (time.time() - start_time))

							#Generate results
							with open(tmp.name, 'a') as f:
								f.write('\n Page {}, status {} on {}'.format(page_instance.url.replace('\r',''),
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
				up_mobile = MobileFriendWeb.objects.get(pk = web_instance.id)
				up_mobile.times_checked += 1
				up_mobile.result = k
				up_mobile.save()
				tmp.close()
			else:
				print('No pages to check....')
				pass


def schedule_mobile_friendly():
	web = MobileFriendWeb.objects.all()
	if web:
		threads = []
		loop = asyncio.new_event_loop().run_until_complete(get_mobile_friendly_api(web))
		asyncio.set_event_loop(loop)
	else:
		print('No web to check.....')
		pass


def schedule_mobile_friendly_rank_checker():
	web = MobileFriendWeb.objects.all()
	if web:
		with httpx.Client() as client:
			print('trigger the day 4 of checking in index....')
			for web_instance in web:
				pages = MobileFriendlyPages.objects.filter(Q(web_id=web_instance.id)).all()
				if pages:
					for page_instance in pages:
						count_days = numOfDays(page_instance.updated_at, datetime.today())
						if count_days >= 7:
							print('day 4 of checking in index....')
							if "'" not in page_instance.url:
								myobj = {
									'keyword': page_instance.url,
									'url': page_instance.url,
									'location': 'Austin, Texas',
								}
								result = client.post("https://ranktracker.applikuapp.com/dataforseo/api/rank-tracker/", json=myobj,
													   headers={'Content-Type': 'application/json',
																'Authorization': 'Token '
																				 'e279b7682f87000aa8d3915702287ce6020a009e'},
													   timeout=300)
								# data = result.json()
								print('data', result)
								if result.status_code == 200 or result.status_code == 201:
									data = result.json()
									if data[0]['status_code'] == 20000:
										result = json.loads(data[0]['json_result'])
										organic = result['tasks'][0]['result'][0]['items']
										index_checker = False
										rank_absolute = None
										for i in organic:
											print(f"URLS: {page_instance.url} vs {i['url']}")
											# url_parsed = urlparse(row['url']) used to parse string url
											# if url == str(url_parsed.netloc) or url == str(row['url']): To check if same domain
											url_1 = page_instance.url
											url_1[-1].replace('/', '')

											url_2 = i['url']
											url_2[-1].replace('/', '')

											if url_1 == url_2:
												page_instance.rank = i['rank_absolute']
												page_instance.rank_group = i['rank_group']
												page_instance.save()
												rank_absolute = i['rank_absolute']
												rank_group = i['rank_group']

										if index_checker:
											print(f"Url {row.url} Indexed with a rank absolute of {rank_absolute} and in the rank group of {rank_group}")
										else:
											# Incomplete Status Code = 0
											page_instance.rank = 300
											page_instance.rank_group = 300
											page_instance.updated_at = timezone.now()
											page_instance.save()
											print(f"Url {page_instance.url} not yet Indexed")
	else:
		print('No web to check.....')
		pass


#SCHEDULE GOOGLE INDEX
def schedule_google_index():
	web = Website.objects.all()
	if web:
		for w in web:
			url = w.website
			SCOPES = ["https://www.googleapis.com/auth/indexing"]
			ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
			index = IndexApi.objects.get(pk=w.indexapi_id)
			JSON_KEY_FILE = index.indexApi
			print(JSON_KEY_FILE)
			# Authorize credentials
			credentials = ServiceAccountCredentials.from_json_keyfile_dict(JSON_KEY_FILE, scopes=SCOPES)
			http = credentials.authorize(httplib2.Http())
			service = build('indexing', 'v3', credentials=credentials)
			batch = service.new_batch_http_request(callback=insert_event2)

			pages = IndexerPages.objects.filter(Q(web_id=w.id) & (Q(index_status__isnull=True) |
																Q(index_status=0) |
																Q(index_status=2)))
			data_arr = []
			try:
				print('this is ', pages.count())
				dt = datetime.now()
				if w.updated_at is None:
					numsite_result = f'\n Updated {pages.count()} pages on {timezone.now()}'
					print(numsite_result)
					w.jsonFile += numsite_result
					w.updated_at = timezone.now()
					w.times_indexed += 1
					w.save()
				else:
					if not dt.strftime("%d/%m/%Y") == w.updated_at.strftime("%d/%m/%Y"):
						numsite_result = f'\n Updated {pages.count()} pages on {timezone.now()}'
						print(numsite_result)
						w.jsonFile += numsite_result
						w.updated_at = timezone.now()
						w.times_indexed += 1
						w.save()

				now = timezone.now()
				for row in pages:
					data_arr.append(row)
					check_dt = IndexerPages.objects.filter(id=row.id, updated_at__isnull=True).first()
					if check_dt:
						batch.add(service.urlNotifications().publish(
							body={"url": row.url.rstrip(), "type": 'URL_UPDATED'}))
						if not check_dt.indexed_date:
							check_dt.indexed_date = timezone.now()
						check_dt.date_tracking = "Last update: {}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
						check_dt.updated_at = timezone.now()
						check_dt.save()
						batch.execute()
					else:
						count_days = numOfDays(row.updated_at, timezone.now())
						print('this is count_days ', count_days)

						# Check if it is in 6 days above
						if not count_days > 6:
							print('check if it is not beyond in 3 days')
							# Check if it is index today
							if not dt.strftime("%d/%m/%Y") == row.updated_at.strftime("%d/%m/%Y"):
								print('check if goes here')
								batch.add(service.urlNotifications().publish(
									body={"url": row.url.rstrip(), "type": 'URL_UPDATED'}))
								result_dt_tracking = "{}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
								upage = IndexerPages.objects.get(pk=row.id)
								if not upage.indexed_date:
									upage.indexed_date = timezone.now()
								upage.date_tracking = 'Last update: ' + upage.date_tracking + "\n" + result_dt_tracking if upage.date_tracking else 'Last update: ' + result_dt_tracking
								upage.save()
								batch.execute()
							else:
								pass
						else:
							pass

				# Check total usage of api
				today = timezone.now()
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
			except:
				if w.updated_at is None:
					w.jsonFile += f'\n Error Updating Indexer Automatically'
					w.save()
				else:
					if not dt.strftime("%d/%m/%Y") == w.updated_at.strftime("%d/%m/%Y"):
						w.jsonFile += f'\n Error Updating Indexer Automatically'
						w.save()
			else:
				pass


#SCHEDULE DAY 4 OF CHECKING INDEX
def every_fourth_day_checking_index():
	web = Website.objects.values_list('id')
	pages = IndexerPages.objects.filter(Q(web_id__in=web) & (Q(index_status__isnull=True) |
															Q(index_status=0) |
															Q(index_status=2)))
	now = timezone.now()
	for row in pages:
		check_dt = IndexerPages.objects.filter(id=row.id, updated_at__isnull=True).first()
		if check_dt:
			check_dt.updated_at = timezone.now()
			if not check_dt.indexed_date:
				check_dt.indexed_date = timezone.now()
			check_dt.date_tracking = "Last update: {}\n".format(now.strftime("%B %d, %Y %H:%M:%S"))
			check_dt.updated_at = timezone.now()
			check_dt.save()
		else:
			count_days = numOfDays(row.updated_at, datetime.today())
			if not count_days > 3:
				print('this is count_days ', count_days)
			elif count_days >= 4:
				print('day 4 of checking in index....')
				if "'" not in row.url:
					myobj = {
						'keyword': f"site:{row.url}",
						'location': 'Austin, Texas',
					}
					print(myobj)
					with httpx.Client() as client:
						result = client.post("https://ranktracker.applikuapp.com/dataforseo/api/search/", json=myobj,
												   headers={'Content-Type': 'application/json',
															'Authorization': 'Token '
																			 'e279b7682f87000aa8d3915702287ce6020a009e'},
												   timeout=300)
						print(result)
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
										row.rank_group = i['rank_group']
										row.save()
										index_checker = True
										rank_absolute = i['rank_absolute']
										rank_group = i['rank_group']

								if index_checker:
									print(f"Url {row.url} Indexed with a rank absolute of {rank_absolute} and in the rank group of {rank_group}")
								else:
									# Incomplete Status Code = 0
									row.index_status = 0
									row.rank_group = 300
									row.updated_at = timezone.now()
									row.save()
									print(f"Url {row.url} not yet Indexed")
				else:
					# Invalid URL Status Code = 2
					row.index_status = 2
					row.rank_group = 300
					row.updated_at = timezone.now()
					row.save()
					print('Skipping invalid URL')