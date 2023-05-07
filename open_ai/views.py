import openai
import os
from dotenv import load_dotenv
import re
from django.http import JsonResponse
from rest_framework import status, authentication
from django.shortcuts import render, redirect
import requests
import json
import base64
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from .models import OpenAiContent, OpenAiKey, OpenAiContentResults, OpenAiAssistedGC, OpenAiAssistedGCHeaders, OpenAiAssistedGCResults, \
	OpenAiPrompt, OpenAiCGPrompt, OpenAiPromptParent, OpenAiPromptSubParent
import os
import asyncio
import httpx
import threading
import time
from googleapiclient.errors import HttpError
from celery import shared_task
from Home.celery import app
from django.db.models import Q, Func, F, Value, CharField, Count, FloatField, Sum
from datetime import datetime, timedelta

load_dotenv()
# Set configurations
key = OpenAiKey.objects.filter(id = 1, status=1).first()
engine = 'text-davinci-003'
temperature = 0.3
max_tokens = 2048
top_p = 0.3
frequency_penalty = 0
presence_penalty = 0


# Function that takes in a prompt, then queries
# OpenAI GPT-3, then returns the completion
def GenerateCompletion(prompt):
	openai.api_key = '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'
	print('api key', openai.api_key)
	return openai.Completion.create(
		engine=engine,
		prompt=prompt,
		temperature=float(temperature),
		max_tokens=int(max_tokens),
		top_p=int(top_p),
		frequency_penalty=int(frequency_penalty),
		presence_penalty=int(presence_penalty)
	)


# Generate the outline of the article using the headers
def GenerateOutline(headers):
	outline = 'Definition'
	for header in headers:
		outline = '{}\n{}'.format(outline, header)
	return outline


# Generate the headers
def GenerateHeaders(keyword):
	headers_prompt = 'For a blog topic "{}", create a logically ordered list in JSON format, of 15 H2 items that ' \
		   'comprehensively cover the blog topic without using any of these words or their variations: {},' \
		   'Introduction, Conclusion, FAQs.'.format(keyword, keyword.replace(' ', ''))
	headers = json.loads(GenerateCompletion(headers_prompt)['choices'][0]['text'])
	return [x['h2'] for x in headers]


# Generate the introduction
def GenerateIntroduction(request, keyword, headers):
	if request.method == 'POST':
		headers = headers.split(',')
		article_content = []
		intro_prompt = OpenAiPrompt.objects.filter(order=1).first()
		data_intro = intro_prompt.prompt
		prompt_intro = data_intro.replace('#KEYWORD', keyword).replace('#HEADER', GenerateOutline(headers))
		intro = GenerateCompletion(prompt_intro)['choices'][0]['text'].strip()
		article_content.append({'Introduction': intro})
		x = OpenAiContent.objects.filter(keyword = keyword, user_id = request.user.id).first()
		if x:
			chck = OpenAiContentResults.objects.filter(results = article_content)
			if not chck:
				OpenAiContentResults.objects.create(
					name = 'Introduction',
					results = article_content,
					order_by = 1,
					content_id = x.id
				)
		return JsonResponse({'content': intro}, safe=True)


# Generate section one
def GenerateFirstSection(request, keyword, title):
	if request.method == 'POST':
		article_content = []
		first_prompt = OpenAiPrompt.objects.filter(order=2).first()
		data_first = first_prompt.prompt
		prompt_one_section = data_first.replace('#KEYWORD', keyword).replace('#HEADER', title)
		first_section = GenerateCompletion(prompt_one_section)['choices'][0]['text'].strip()
		article_content.append({title: first_section})
		c = OpenAiContent.objects.filter(keyword = keyword, user_id = request.user.id).first()
		if c:
			chck = OpenAiContentResults.objects.filter(results = article_content)
			if not chck:
				OpenAiContentResults.objects.create(
					name = 'First Section',
					results = article_content,
					order_by = 2,
					content_id = c.id
				)
		return JsonResponse({'content': first_section}, safe=True)


# Generate other sections
def GenerateOtherSections(request, keyword, title, previous_title):
	if request.method == 'POST':
		article_content = []
		second_prompt = OpenAiPrompt.objects.filter(order=3).first()
		data_two = second_prompt.prompt
		prompt_other_section = data_two.replace('#KEYWORD', keyword).replace('#PREV_HEADER', previous_title).replace('#HEADER', title)
		other_sections = GenerateCompletion(prompt_other_section)['choices'][0]['text'].strip()
		article_content.append({title: other_sections})
		b = OpenAiContent.objects.filter(keyword = keyword, user_id = request.user.id).first()
		if b:
			chck = OpenAiContentResults.objects.filter(results = article_content)
			if not chck:
				OpenAiContentResults.objects.create(
					name = 'Other Section',
					results = article_content,
					order_by = 3,
					content_id = b.id
				)
		return JsonResponse({'content': other_sections}, safe=True)


# Generate the conclusion
def GenerateConclusion(request, keyword, headers):
	if request.method == 'POST':
		headers = headers.split(',')
		article_content = []
		con_prompt = OpenAiPrompt.objects.filter(order=4).first()
		data_con = con_prompt.prompt
		prompt_con = data_con.replace('#KEYWORD', keyword).replace('#HEADER', GenerateOutline(headers))
		conclusions = GenerateCompletion(prompt_con)['choices'][0]['text'].strip()
		article_content.append({'Conclusion': conclusions})
		b = OpenAiContent.objects.filter(keyword = keyword, user_id = request.user.id).first()
		if b:
			b.status = 'Done'
			b.save()
			chck = OpenAiContentResults.objects.filter(results = article_content)
			if not chck:
				OpenAiContentResults.objects.create(
					name = 'Conclusion',
					results = article_content,
					order_by = 4,
					content_id = b.id
				)
		return JsonResponse({'content': conclusions}, safe=True)


@login_required()
@csrf_exempt
def user_open_ai(request):
	if request.method == 'POST':
		print(request.POST.get('message'))
		article_db = OpenAiContent.objects.filter(keyword = request.POST.get('message'), user_id = request.user.id).first()
		if not article_db:
			content = OpenAiContent(
				keyword = request.POST.get('message'),
				user_id = request.user.id,
				status = 'Generating'
			)
			content.save()
		headers = GenerateHeaders(request.POST.get('message'))
		print('headers', headers)
		return JsonResponse({'article_headers': headers}, safe=True)

	context = {
		'active_tab': 'open_ai',
	}
	return render(request, 'indexer-user/open_ai/open_ai.html', context)


@login_required()
@csrf_exempt
def user_open_ai_logs(request):
	context = {
		'active_tab': 'content_logs',
		'prompt': OpenAiPromptParent.objects.filter(status=1).all()
	}
	return render(request, 'indexer-user/open_ai/open_ai_logs.html', context)


@login_required()
@csrf_exempt
def user_open_ai_view_logs(request, pk):
	if request.method == 'POST':
		try:
			article_db = OpenAiContent.objects.filter(id = pk).first()
			if article_db:
				article_db.keyword = request.POST.get('up_message')
				article_db.status = 'Generating'
				article_db.save()
				prompt = request.POST.get('up_prompts')
				if prompt:
					print('prompt', prompt)
					pr = OpenAiCGPrompt.objects.filter(cg_id = pk).first()
					pr.prompt_id = request.POST.get('up_prompts')
					pr.save()
			return JsonResponse({'data': 'success', 'msg': 'Keyword sucessfully updated for the content. Please dont refresh the page and wait for the result since the it is \
						in schedule for generating. Thanks!'})
		except requests.exceptions.HTTPError as err:
			if err.response.status_code == 524:
				# Handle the 524 error here
				print("Server responded with a 524 error.")
				return JsonResponse({'data': 'error', 'msg': 'Server responded with a 524 error.'})
			else:
				# Handle other HTTP errors here
				print(f"HTTP error occurred: {err}")
				return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
		except Exception as err:
			# Handle other exceptions here
			print(f"An error occurred: {err}")
			return JsonResponse({'data': 'error', 'msg': f"An error occurred: {err}"})
	context = {
		'content' : OpenAiContent.objects.filter(id = pk).first(),
		'prompt': OpenAiPromptParent.objects.filter(status=1).all(),
		'cg_prompt': OpenAiCGPrompt.objects.filter(cg_id = pk).first(),
		'pk': pk
	}
	return render(request, 'indexer-user/open_ai/open_ai_logs_view_prompt.html', context)


@login_required()
@csrf_exempt
def create_generate_content(request):
	try:
		article_db = OpenAiContent.objects.filter(keyword = request.POST.get('message'), user_id = request.user.id).first()
		if not article_db:
			content = OpenAiContent(
				keyword = request.POST.get('message'),
				user_id = request.user.id,
				status = 'Generating'
			)
			content.save()
			prompt = request.POST.get('prompts')
			print('this is ', prompt)
			if prompt:
				OpenAiCGPrompt.objects.create(
					prompt_id = prompt,
					cg_id = content.id
				)
					
		# headers = GenerateArticle(request.POST.get('message'))
		# headers = app.send_task('indexer.tasks.GenerateArticle', args=[request.POST.get('message')])
		# print('headers', headers)
		return JsonResponse({'data': 'success', 'msg': 'Keyword sucessfully created for the content. Please dont refresh the page and wait for the result since the it is \
					in schedule for generating. Thanks!'})
	except requests.exceptions.HTTPError as err:
		if err.response.status_code == 524:
			# Handle the 524 error here
			print("Server responded with a 524 error.")
			return JsonResponse({'data': 'error', 'msg': 'Server responded with a 524 error.'})
		else:
			# Handle other HTTP errors here
			print(f"HTTP error occurred: {err}")
			return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
	except Exception as err:
		# Handle other exceptions here
		print(f"An error occurred: {err}")
		return JsonResponse({'data': 'error', 'msg': f"An error occurred: {err}"})


@login_required()
@csrf_exempt
def user_open_ai_content_view(request, pk):
	context = {
		'article':  OpenAiContent.objects.filter(id = pk).first(),
		'intro': OpenAiContentResults.objects.filter(content_id = pk, order_by=1).first(),
		'first_section': OpenAiContentResults.objects.filter(content_id = pk, order_by=2).first(),
		'other_section': OpenAiContentResults.objects.filter(content_id = pk, order_by=3).all(),
		'conclusion': OpenAiContentResults.objects.filter(content_id = pk, order_by=4).first()
	}
	return render(request, 'indexer-user/open_ai/open_ai_view_content.html', context)

def PassingContentGenerated(request, keyword, pk, prompt_id):
	while True:
		#Initiate variables
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
		else:
			print('no data found in headers...')
		time.sleep(3)
		break
	return True

# ASSISTED GC
@login_required()
@csrf_exempt
def user_open_ai_assisted_gc(request):
	if request.method == 'POST':
		print(request.POST.get('title'))
		try:
			article_db = OpenAiAssistedGC.objects.filter(title = request.POST.get('title'), user_id = request.user.id).first()
			if not article_db:
				content = OpenAiAssistedGC(
					title = request.POST.get('title'),
					user_id = request.user.id,
					status = 1,
					prompt_id = request.POST.get('prompts'),
					is_cg = 1 if request.POST.get('prompts') == '2' else None,
					cg_status = 'Generating'
				)
				content.save()
				if request.POST.get('prompts') == '2':
					threads = []
					t = threading.Thread(target=PassingContentGenerated, args=(request, request.POST.get('title'), 
								content.id, request.POST.get('prompts')), daemon=True)
					t.start()
					threads.append(t)
					for thread in threads:
						thread.join()
					content.cg_status = 'Done'
					content.save()
			return JsonResponse({'data': 'success'})
		except requests.exceptions.HTTPError as err:
			return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
		except HttpError as error:
			# Handle the HttpError exception
			print(f'An HTTP error occurred: {error}')
			print(f'Status code: {error.resp.status}')
			print(f'Error content: {error.content}')
			return JsonResponse({'data': 'error', 'msg': {error.resp.status}})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	context = {
		'active_tab': 'assisted_gc',
		'prompt': OpenAiPromptParent.objects.filter(status=1).all()
	}
	return render(request, 'indexer-user/open_ai/open_ai_assisted_gc.html', context)


@login_required()
@csrf_exempt
def user_open_ai_assisted_gc_view_prompt(request, pk):
	if request.method == 'POST':
		try:
			ass = OpenAiAssistedGC.objects.filter(id = pk).first()
			if ass:
				ass.title = request.POST.get('up_title')
				ass.status = 1 if request.POST.get('up_status') else 0
				ass.prompt_id = request.POST.get('up_prompts')
				ass.save()
				check = OpenAiAssistedGCHeaders.objects.filter(ass_id = pk)
				if check:
					print('naa....')
					for data in check:
						data.status = 'Pending'
						data.save()
			return JsonResponse({'data': 'success', 'msg': 'Informations sucessfully updated for the content.'})
		except requests.exceptions.HTTPError as err:
			if err.response.status_code == 524:
				# Handle the 524 error here
				print("Server responded with a 524 error.")
				return JsonResponse({'data': 'error', 'msg': 'Server responded with a 524 error.'})
			else:
				# Handle other HTTP errors here
				print(f"HTTP error occurred: {err}")
				return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
		except Exception as err:
			# Handle other exceptions here
			print(f"An error occurred: {err}")
			return JsonResponse({'data': 'error', 'msg': f"An error occurred: {err}"})
	context = {
		'ass': OpenAiAssistedGC.objects.filter(id = pk).first(),
		'pk': pk,
		'prompt': OpenAiPromptParent.objects.filter(status=1).all()
	}
	return render(request, 'indexer-user/open_ai/open_ai_assisted_gc_view_prompt.html', context)

@login_required()
@csrf_exempt
def user_open_ai_assisted_gc_generate_headers(request):
	if request.method == 'POST':
		try:
			if request.POST.get('headers'):
				for row in request.POST.get('headers').split('\n'):
					print(row.rstrip())
					check_page = OpenAiAssistedGCHeaders.objects.filter(Q(ass_id=request.POST.get('pk')) & Q(headers=row.rstrip()))
					if check_page:
						print('duplicate found...')
						pass
					else:
						if not check_page:
							hdrs = OpenAiAssistedGCHeaders(
								headers = row.rstrip(),
								ass_id = request.POST.get('pk'),
								status = 'Pending',
							)
							hdrs.save()
				return JsonResponse({'data': 'success','msg': 'Headers successfully created.'})
		except requests.exceptions.HTTPError as err:
			return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
		except HttpError as error:
			# Handle the HttpError exception
			print(f'An HTTP error occurred: {error}')
			print(f'Status code: {error.resp.status}')
			print(f'Error content: {error.content}')
			return JsonResponse({'data': 'error', 'msg': {error.resp.status}})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})


def PassingAssistedGenerateContent(request, keyword, pk, prompt_id):
	while True:
		# Initialize variable to store the contents of the articles
		print('this is prompt', prompt_id)
		all_data = OpenAiAssistedGCHeaders.objects.filter(Q(ass_id=pk) & ~Q(status='Done')).all().order_by('id')
		headers = [x.id for x in all_data]
		print('headers', headers[0])

		sub_parent_prompt = OpenAiPromptSubParent.objects.filter(parent_id=prompt_id).order_by('prompt_id')
		print('sub_parent_prompt', sub_parent_prompt)
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
		time.sleep(3)
		break
	return True		

@login_required()
@csrf_exempt
def GenerateFirstSectionAndOtherSections(request):
	try:
		print('this is pk', request.POST.get('pk'))
		keyword = OpenAiAssistedGC.objects.get(Q(pk = request.POST.get('pk')) & ~Q(is_cg=1) & Q(cg_status='Generating'))
		threads = []
		t = threading.Thread(target=PassingAssistedGenerateContent, args=(request, keyword.title, request.POST.get('pk'), keyword.prompt.id), daemon=True)
		t.start()
		threads.append(t)
		for thread in threads:
			thread.join()
		keyword.cg_status = 'Done'
		keyword.save()
		return JsonResponse({'data': 'success'})
		# from apscheduler.schedulers.background import BackgroundScheduler
		# scheduler = BackgroundScheduler()
		# print('this is pk', request.POST.get('pk'))
		# keyword = OpenAiAssistedGC.objects.get(pk = request.POST.get('pk'))
		# scheduler.add_job(PassingAssistedGenerateContent(request, keyword.title, request.POST.get('pk'), keyword.prompt.id), 'interval', seconds=15)
		# scheduler.start()
		# while True:
		# 	time.sleep(1)
	except requests.exceptions.HTTPError as err:
		return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
	except HttpError as error:
		# Handle the HttpError exception
		print(f'An HTTP error occurred: {error}')
		print(f'Status code: {error.resp.status}')
		print(f'Error content: {error.content}')
		return JsonResponse({'data': 'error', 'msg': {error.resp.status}})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': str(e)})


@login_required()
@csrf_exempt
def user_open_ai_assisted_gc_view_results(request, pk):
	context = {
		'title': OpenAiAssistedGC.objects.filter(pk = pk).first(),
		'intro': OpenAiAssistedGCResults.objects.filter(headers__ass_id = pk, order_by=1).first(),
		'conclusion': OpenAiAssistedGCResults.objects.filter(headers__ass_id = pk, order_by=4).first(),
		'first_section': OpenAiAssistedGCResults.objects.filter(headers__ass_id = pk, order_by=2).first(),
		'other_section': OpenAiAssistedGCResults.objects.values('results').filter(headers__ass_id = pk, order_by=3).annotate(count=Count('headers_id')).all(),
	}
	return render(request, 'indexer-user/open_ai/open_ai_assisted_gc_view_results.html', context)


@login_required()
@csrf_exempt
def user_open_ai_content_view_headers(request, pk):
	context = {
		'headers': OpenAiAssistedGCHeaders.objects.filter(pk = pk).first(),
		'intro': OpenAiAssistedGCResults.objects.filter(headers_id = pk, order_by=1).first(),
		'first_section': OpenAiAssistedGCResults.objects.filter(headers_id = pk, order_by=2).first(),
		'other_section': OpenAiAssistedGCResults.objects.filter(headers_id = pk, order_by=3).first(),
	}
	return render(request, 'indexer-user/open_ai/open_ai_generate_headers_content.html', context)


@login_required()
@csrf_exempt
def user_open_ai_prompt(request):
	if request.method == 'POST':
		try:
			prompt = OpenAiPrompt.objects.filter(name = request.POST.get('name')).first()
			if not prompt:
				pr = OpenAiPrompt(
					name = request.POST.get('name'),
					prompt = request.POST.get('prompt'),
					order = request.POST.get('order'),
					status = 1 if request.POST.get('status') else 0
				)
				pr.save()
			return JsonResponse({'data': 'success','msg': 'Prompt successfully saved.'})
		except requests.exceptions.HTTPError as err:
			return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
		except HttpError as error:
			# Handle the HttpError exception
			print(f'An HTTP error occurred: {error}')
			print(f'Status code: {error.resp.status}')
			print(f'Error content: {error.content}')
			return JsonResponse({'data': 'error', 'msg': {error.resp.status}})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	context = {
		'active_tab': 'prompt'
	}
	return render(request, 'indexer-user/open_ai/open_ai_prompt.html', context)

@login_required()
@csrf_exempt
def user_open_ai_prompt_update(request, pk):
	if request.method == 'POST':
		try:
			up_prompt = OpenAiPrompt.objects.filter(id = pk).first()
			check = OpenAiPrompt.objects.filter(Q(name=request.POST.get('edit-name')) & ~Q(name=up_prompt.name))
			if check:
				return JsonResponse({'data': 'error', 'msg': 'Prompt name already exist.'})
			else:
				up_prompt.name = request.POST.get('edit-name')
				up_prompt.prompt = request.POST.get('edit-prompt') 
				up_prompt.order = request.POST.get('edit-order')
				up_prompt.status = 1 if request.POST.get('edit-status') else 0
				up_prompt.updated_at = datetime.now()
				up_prompt.save()
				return JsonResponse({'data': 'success','msg': 'Prompt successfully updated.'})
		except requests.exceptions.HTTPError as err:
			return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
		except HttpError as error:
			# Handle the HttpError exception
			print(f'An HTTP error occurred: {error}')
			print(f'Status code: {error.resp.status}')
			print(f'Error content: {error.content}')
			return JsonResponse({'data': 'error', 'msg': {error.resp.status}})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	context = {
		'prompt': OpenAiPrompt.objects.get(pk = pk),
		'pk': pk
	}
	return render(request, 'indexer-user/open_ai/open_ai_prompt_view.html', context)


@login_required()
@csrf_exempt
def user_open_ai_prompt_parent(request):
	if request.method == 'POST':
		try:
			prompt = OpenAiPromptParent.objects.filter(name = request.POST.get('name')).first()
			if not prompt:
				pr = OpenAiPromptParent(
					name = request.POST.get('name'),
					status = 1 if request.POST.get('status') else 0
				)
				pr.save()
				for row in request.POST.getlist('prompts'):
					OpenAiPromptSubParent.objects.create(
						parent_id = pr.id,
						prompt_id = row
					)
			return JsonResponse({'data': 'success','msg': 'Prompt parent successfully saved.'})
		except requests.exceptions.HTTPError as err:
			return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
		except HttpError as error:
			# Handle the HttpError exception
			print(f'An HTTP error occurred: {error}')
			print(f'Status code: {error.resp.status}')
			print(f'Error content: {error.content}')
			return JsonResponse({'data': 'error', 'msg': {error.resp.status}})
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	context = {
		'active_tab': 'prompt_parent',
		'prompt': OpenAiPrompt.objects.filter(status=1).all()
	}
	return render(request, 'indexer-user/open_ai/open_ai_prompt_parent.html', context)


@login_required()
@csrf_exempt
def user_open_ai_prompt_parent_view(request, pk):
	if request.method == 'POST':
		try:
			parent = OpenAiPromptParent.objects.filter(id = pk).first()
			check_parent_prompt = OpenAiPromptParent.objects.filter(name = request.POST.get('up_name')).first()
			if not check_parent_prompt:
				parent.name = request.POST.get('up_name')
				parent.status = 1 if request.POST.get('up_status') else 0
				parent.save()
				prompt = request.POST.getlist('up_prompts')
				if prompt:
					for data in prompt:
						print('this is row', data)
						check_prompt = OpenAiPromptSubParent.objects.filter(prompt_id = data, parent_id = pk)
						if not check_prompt:
							OpenAiPromptSubParent.objects.create(
								prompt_id = data,
								parent_id = pk
							)
			# headers = GenerateArticle(request.POST.get('message'))
			# headers = app.send_task('indexer.tasks.GenerateArticle', args=[request.POST.get('message')])
			# print('headers', headers)
			return JsonResponse({'data': 'success', 'msg': 'Promp parent successfully updated.'})
		except requests.exceptions.HTTPError as err:
			if err.response.status_code == 524:
				# Handle the 524 error here
				print("Server responded with a 524 error.")
				return JsonResponse({'data': 'error', 'msg': 'Server responded with a 524 error.'})
			else:
				# Handle other HTTP errors here
				print(f"HTTP error occurred: {err}")
				return JsonResponse({'data': 'error', 'msg': f"HTTP error occurred: {err}"})
		except Exception as err:
			# Handle other exceptions here
			print(f"An error occurred: {err}")
			return JsonResponse({'data': 'error', 'msg': f"An error occurred: {err}"})
	context = {
		'parent' : OpenAiPromptParent.objects.filter(id = pk).first(),
		'prompt': OpenAiPrompt.objects.filter(status=1).all(),
		'sub_parent': OpenAiPromptSubParent.objects.filter(parent_id=pk),
		'pk': pk
	}
	return render(request, 'indexer-user/open_ai/open_ai_prompt_parent_view.html', context)