import re
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
import json
import base64
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CloudflareModel, CloudflareDNSInfo, CloudflareModelUrl, CloudflarePageRule
from urllib import response
from django.db import models
from django.conf import settings
from apps.utils.models import BaseModel
from CloudFlare import CloudFlare
from client.models import ClientSettings, CloudflareWebsites
from django.db.models import Q
from datetime import datetime, timedelta
# Create your views here.

@login_required()
@csrf_exempt
def cloud_fare_api(request):
	client_settings = ClientSettings.objects.get(user=request.user)
	token = client_settings.access_token
	if request.method == 'POST':
		try:
			print(request.POST.get('keys'))
			cf = CloudFlare(email=request.POST.get('email'), token=request.POST.get('keys'))
			zones = cf.zones.get(params = {'per_page':100})
			sites = ''
			for zone in zones:
				zone_name = zone['name']
				sites += f"{zone_name}\n"
			chk_cloudflare = CloudflareModel.objects.filter(email = request.POST.get('email'), user_id = request.user.id).first()
			if not chk_cloudflare:
				cloudflare = CloudflareModel(
					email = request.POST.get('email'),
					key = request.POST.get('keys'),
					nameServers = request.POST.get('nameServers'),
					account_id = request.POST.get('acc_id'),
					account_token = request.POST.get('acc_token'),
					user_id = request.user.id,
					status = 1 if request.POST.get('email') else 0,
					resP = sites 
				)
				cloudflare.save()
				data = {
					'email': request.POST.get('email'),
					'account_id': request.POST.get('acc_id'),
					'account_token': request.POST.get('acc_token'),
					'api_key': request.POST.get('keys'),
				}
				req = requests.post("http://95.217.184.122/api/cloudflare/", headers={'Authorization': f'Bearer {token}'},
                                        json=data)
				if req.status_code == 200 or req.status_code == 201:
					for z in zones:
						cl_url = CloudflareModelUrl(
							cloudfare_model_id = cloudflare.id,
							zone_id = z['id'],
							zone_name = z['name']
						)
						cl_url.save()
			return JsonResponse({'data': 'success', 'msg': 'Successfully saved the cloudflare api.'}, safe=True)
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	context = {
		'active_tab': 'user_api',
	}
	return render(request, 'indexer-user/cloud_flare/user_api.html', context)


@login_required()
@csrf_exempt
def generate_updated_sites(request):
	cloudflare_api_info = CloudflareModel.objects.get(pk = request.POST.get('pk'))
	cf = CloudFlare(email=cloudflare_api_info.email, token=cloudflare_api_info.key)
	zones = cf.zones.get(params = {'per_page':100})
	for zone in zones:
		check_url = CloudflareModelUrl.objects.filter(zone_name = zone['name'])
		if not check_url:
			cl_url = CloudflareModelUrl(
				cloudfare_model_id = request.POST.get('pk'),
				zone_id = zone['id'],
				zone_name = zone['name']
			)
			cl_url.save()
	return JsonResponse({'data': 'success', 'msg': 'Successfully updated the sites.'}, safe=True)


@login_required()
@csrf_exempt
def add_sites(request):
	if request.method == 'POST':
		try:
			# Assuming the user's Cloudflare API info is stored in the CloudflareAPIInfo model
			cloudflare_api_info = CloudflareModel.objects.get(pk = request.POST.get('pk'))
			cf = CloudFlare(email=cloudflare_api_info.email, token=cloudflare_api_info.key)
			# Get the site details from the form data
			for row in request.POST.get('sites').split('\n'):
			# Make API request to create a new site
				zones = cf.zones.post(data={"name": row})
				print('zones', zones)
				print('zones id', zones['id'])
				print('zones name', zones['name'])
				#Inser the model database the generating results of cloudflare.
				cl_url = CloudflareModelUrl(
					cloudfare_model_id = request.POST.get('pk'),
					zone_id = zones['id'],
					zone_name = zones['name']
				)
				cl_url.save()
			# Optionally, you can process the API response and handle any errors
			return JsonResponse({'data': 'success', 'msg': 'Successfully created new sites.'}, safe=True)
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	

@login_required()
def edit_dns(request, pk):
	# Assuming the user's Cloudflare API info is stored in the CloudflareAPIInfo model
	cloudflare_api_info = CloudflareModelUrl.objects.get(pk = pk)
	print(cloudflare_api_info.zone_id)
	cf = CloudFlare(email=cloudflare_api_info.cloudfare_model.email, token=cloudflare_api_info.cloudfare_model.key)
	# Make API request to fetch existing DNS information for the site
	zone_id = cloudflare_api_info.zone_id
	dns_records = cf.zones.dns_records.get(zone_id)
	if request.method == 'POST':
		try:
			check_dns = CloudflareDNSInfo.objects.filter(name=request.POST['name'])
			if not check_dns:
				data = {
					'name': request.POST['name'],
					'type': request.POST['type'],
					'content': request.POST['content']
				}
				# Create the new DNS record using the Cloudflare API
				result = cf.zones.dns_records.post(zone_id, data=data)
				if result:
					dns_record_info = CloudflareDNSInfo(
						cloudflare_url_id = pk,
						record_id = result['id'],
						name = data['name'],
						type = data['type'],
						content = data['content']
					)
					dns_record_info.save()
					return JsonResponse({'data': 'success', 'msg': 'Successfully created new dns.'}, safe=True)
			else:
				return JsonResponse({'data': 'error', 'msg': 'Dns duplicated. Please try new one.'}, safe=True)
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	context = {
		'dns_records': dns_records,
		'pk': pk,
		'model_id': cloudflare_api_info.cloudfare_model.id
	}
	return render(request, 'indexer-user/cloud_flare/users_view_dns.html', context)


@login_required()
def page_rule(request, pk):
	# Assuming the user's Cloudflare API info is stored in the CloudflareAPIInfo model
	cloudflare_api_info = CloudflareModelUrl.objects.get(pk = pk)
	print(cloudflare_api_info.zone_id)
	cf = CloudFlare(email=cloudflare_api_info.cloudfare_model.email, token=cloudflare_api_info.cloudfare_model.key)
	# Make API request to fetch existing DNS information for the site
	zone_id = cloudflare_api_info.zone_id
	if request.method == 'POST':
		try:
			# Get the data from the form
			if request.POST.get('rule_id') == '':
				print('create rule...')
				url_pattern = request.POST.get('url_pattern')
				action = request.POST.get('action')
				priority = request.POST.get('priority')
				page_rule = {
					'targets': [{'target': 'url', 'constraint': {'operator': 'matches', 'value': url_pattern}}],
					'actions': [{"id":action,"value":{"status_code":301,"url":f"https://www.{cloudflare_api_info.zone_name}/$1"}}],
					'priority': priority,
					'status': 'active',
				}
				result = cf.zones.pagerules.post(zone_id, data=page_rule)
				print('results', result)
				# If successful, save the rule in the database
				if result:
					CloudflarePageRule.objects.create(
						resp_url_id = pk,
						zone_id=zone_id,
						rule_id=result['id'],
						targets=url_pattern,
						actions=action,
						priority=priority,
						resp=result
					)
					return JsonResponse({'data': 'success', 'msg': 'Successfully created page rule.'}, safe=True)
			else:
				print('update rule...')
				rule_id = request.POST.get('rule_id')
				url_pattern = request.POST.get('url_pattern')
				action = request.POST.get('action')
				priority = request.POST.get('priority')
				page_rule = {
					'targets': [{'target': 'url', 'constraint': {'operator': 'matches', 'value': url_pattern}}],
					'actions': [{"id":action,"value":{"status_code":301,"url":f"https://www.{cloudflare_api_info.zone_name}/$1"}}],
					'priority': priority,
					'status': 'active',
				}
				result = cf.zones.pagerules.put(zone_id, rule_id, data=page_rule)
				print('results', result)
				if result:
					page_rule = CloudflarePageRule.objects.filter(Q(id = request.POST.get('pk')) & Q(rule_id=rule_id)).first()
					if page_rule:
						page_rule.targets = url_pattern
						page_rule.actions = action
						page_rule.priority = priority
						page_rule.resp = result
						page_rule.save()
				return JsonResponse({'data': 'success', 'msg': 'Successfully updated page rule.'}, safe=True)
		except CloudFlare.CloudFlareAPIError as e:
			return JsonResponse({'data': 'error', 'msg': f'Error creating page rule: {e}'})
	context = {
		'pk': pk,
		'model_id': cloudflare_api_info.cloudfare_model.id
	}
	return render(request, 'indexer-user/cloud_flare/users_page_rule.html', context)


@login_required
@csrf_exempt
def delete_dns_record(request):
	try:
		cloudflare_api_info = CloudflareModelUrl.objects.get(pk = request.POST.get('pk'))
		cf = CloudFlare(email=cloudflare_api_info.cloudfare_model.email, token=cloudflare_api_info.cloudfare_model.key)
		zone_id = cloudflare_api_info.zone_id
		print('zone_id', zone_id)
		print('pk', request.POST.get('pk'))
		print('record id', request.POST.get('record_id'))
		# Delete the DNS record using the Cloudflare API
		result = cf.zones.dns_records.delete(zone_id, request.POST.get('record_id'))
		# If successful, delete the record from the database
		if result:
			dns_record = CloudflareDNSInfo.objects.filter(record_id=request.POST.get('record_id')).first()
			if dns_record:
				dns_record.delete()
		return JsonResponse({'data': 'success', 'msg': 'Data successfully deleted!'})
	except Exception as e:
		return JsonResponse({'data': 'error', 'msg': str(e)})


@login_required()
@csrf_exempt
def edit_dns_record(request, record_id, pk):
	cloudflare_api_info = CloudflareModelUrl.objects.get(pk = pk)
	cf = CloudFlare(email=cloudflare_api_info.cloudfare_model.email, token=cloudflare_api_info.cloudfare_model.key)
	zone_id = cloudflare_api_info.zone_id
	dns_record = cf.zones.dns_records.get(zone_id, record_id)
	if request.method == 'POST':
		try:
			data = {
				'name': request.POST['name'],
				'type': request.POST['type'],
				'content': request.POST['content']
			}
			# Update the DNS record using the Cloudflare API
			result = cf.zones.dns_records.put(zone_id, record_id, data=data)
			# If successful, update the record in the database
			if result:
				check_dns = CloudflareDNSInfo.objects.filter(name=data['name'])
				if not check_dns:
					dns_record_info = CloudflareDNSInfo(
						cloudflare_url_id = pk,
						name = data['name'],
						type = data['type'],
						content = data['content']
					)
					dns_record_info.save()
				return JsonResponse({'data': 'success', 'msg': 'Successfully updated the dns.'}, safe=True)
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	context = {
		'record_id': record_id,
		'pk': pk,
		'dns_record': dns_record
	}
	return render(request, 'indexer-user/cloud_flare/users_edit_dns_info.html', context)


@login_required()
@csrf_exempt
def cloud_fare_api_view_sites(request, pk):
	if request.method == 'POST':
		return JsonResponse({'data': 'success', 'msg': 'Successfully saved the cloudflare api.'}, safe=True)
	cloud_flare = CloudflareModel.objects.get(pk = pk)
	context = {
		'cloud_flare': cloud_flare,
		'pk': pk
	}
	return render(request, 'indexer-user/cloud_flare/user_view_sites.html', context)


@login_required()
@csrf_exempt
def cloud_fare_api_view(request, pk):
	if request.method == 'POST':
		try:
			cloud_flare_update = CloudflareModel.objects.get(pk = pk)
			cloud_flare_update.email = request.POST.get('up_email')
			cloud_flare_update.key = request.POST.get('up_keys')
			cloud_flare_update.nameServers = request.POST.get('up_nameServers')
			cloud_flare_update.account_id = request.POST.get('up_acc_id')
			cloud_flare_update.account_token = request.POST.get('up_acc_token')
			cloud_flare_update.status = 1 if request.POST.get('up_status') else 0
			cloud_flare_update.updated_at = datetime.now()
			cloud_flare_update.save()
			return JsonResponse({'data': 'success', 'msg': 'Successfully updated the cloudflare api.'}, safe=True)
		except Exception as e:
			return JsonResponse({'data': 'error', 'msg': str(e)})
	cloud_flare = CloudflareModel.objects.get(pk = pk)
	print('this is', cloud_flare.resP)
	context = {
		'cloud_flare': cloud_flare,
		'pk': pk
	}
	return render(request, 'indexer-user/cloud_flare/user_api_view.html', context)