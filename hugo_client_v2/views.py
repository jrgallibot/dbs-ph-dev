from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from client.models import ClientSettings, CloudflareWebsites, MaintenanceStatus, ClientComments, ClientPostSched, ClientPbnGroup, ClientWebsitePbnGroup
from indexer.models import IndexApi
from Cloudflare.models import CloudflareModel
from django.views.decorators.http import require_POST
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt
from io import TextIOWrapper
import re
import requests
import csv


def get_token(request):
    client_settings = ClientSettings.objects.get(user=request.user)
    return client_settings.access_token


def index_page(request):
    try:
        token = get_token(request)
        context = {'title': 'Hugo Client', 'module_name': 'Hugo',
                   'data': requests.get("http://127.0.0.1:7000/api/home-page/",
                                        headers={'Authorization': f'Bearer {token}'}).json(), 'active_tab': 'hugo_v2'}

        return render(request, 'hugo_v2/index.html', context)
    except Exception as e:
        print(e)


@require_POST
def add_website_page(request):
    try:
        token = get_token(request)
        data = {
            'title': request.POST.get('title'),
            'base_url': request.POST.get('base_url'),
            'language_code': request.POST.get('language_code'),
            'theme': request.POST.get('theme'),
            'description': request.POST.get('description'),
            'page_name': request.POST.get('page_name')
        }
        req = requests.post("http://127.0.0.1:7000/api/website-v2/", headers={'Authorization': f'Bearer {token}'}, json=data)
        print(req.status_code)
        if req.status_code == 200 or req.status_code == 201:
            return redirect('/hugo-client-v2/')
    except Exception as e:
        print(e)

def website_page(request, pk):
    try:
        token = get_token(request)
        context = {
            'title': 'Hugo Client', 
            'module_name': 'Hugo',
            'website_id': str(pk),
            'data': requests.get(f"http://127.0.0.1:7000/api/site-page-v2/{pk}/",
                                                   headers={'Authorization': f'Bearer {token}'}).json(),
            'cloudflare': CloudflareModel.objects.filter(user=request.user).all(),
        }
        return render(request, 'hugo_v2/partials/site.html', context)
    except Exception as e:
        print(e)


@require_POST
def add_page(request, pk):
    try:
        token = get_token(request)
        data = {
            'website': str(pk),
            'page': request.POST.get('page'),
            'slug': request.POST.get('slug'),
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'description': request.POST.get('description'),
            'tags': request.POST.get('tags'),
            'categories': request.POST.get('categories'),
            'keywords': request.POST.get('keywords'),
            'in_navbar': True if request.POST.get('in_navbar') == "on" else False,
        }
        req = requests.post(f"http://127.0.0.1:7000/api/add-page-v2/",
                            headers={'Authorization': f'Bearer {token}'}, json=data)
        if req.status_code == 200 or req.status_code == 201:
            return JsonResponse({'data': req.text, 'website_id': str(pk)}, status=200)
        else:
            return JsonResponse({'statusMsg': req.text}, status=404)
    except Exception as e:
        print(e) 

def publish_website_page(request, wid):
    try:
        token = get_token(request)
        cloudflare = CloudflareModel.objects.get(id=request.POST.get('cloudflare'), user=request.user)
        data = {
            'account_id': cloudflare.account_id,
            'account_token': cloudflare.account_token,
            'api_key': cloudflare.key,
            'email': cloudflare.email,
            'domain': request.POST.get('domain'),
            'page_name': request.POST.get('page_name'),
        }
        print(data)
        req = requests.post(
            f"http://127.0.0.1:7000/api/publish-website-v2/{wid}/",
            headers={'Authorization': f'Bearer {token}'}, data=data)
        print(req.text)
        context = {}
        if req.status_code == 200 or req.status_code == 201:
            cfw = CloudflareWebsites.objects.filter(website_id=wid).first()
            if cfw:
                cfw.cloudflare = cloudflare
                cfw.save()
            else:
                CloudflareWebsites.objects.create(website_id=wid, cloudflare=cloudflare)
            messages.success(request, 'You have successfully published a website.')
            context['data'] = {
                'website': req.json()['data']
            }
            context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
            return render(request, 'hugo_v2/partials/site-cloudflare-details-card.html', context)
        else:
            context['data'] = {
                'website': req.json()['data']
            }
            print(req)
            context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
            messages.error(request, req.json()['statusMsg'])
            return render(request, 'hugo_v2/partials/site-cloudflare-details-card.html', context)
    except Exception as e:
        print(e)
        return JsonResponse({'statusMsg': str(e)}, status=404)

def update_page(request, wid):
    try:
        if request.method == "POST":
            token = get_token(request)
            data = {   
                'website': str(wid),
                'page_id': request.POST.get('page_id'),
                'page': request.POST.get('page'),
                'slug': request.POST.get('slug'),
                'title': request.POST.get('title'),
                'tags': request.POST.get('tags'),
                'categories': request.POST.get('categories'),
                'keywords': request.POST.get('keywords'),
                'content': request.POST.get('content'),
                'description': request.POST.get('description'),
                'in_navbar': True if request.POST.get('in_navbar') == "on" else False,
                'date_published': request.POST.get('date_published')
            }
            req = requests.post(f"http://127.0.0.1:7000/api/update-page-v2/{str(wid)}/{request.POST.get('page_id')}/", headers={'Authorization': f'Bearer {token}'}, json=data)
            if req.status_code == 200 or req.status_code == 201:
                return JsonResponse({'data': req.text, 'website_id': str(wid)}, status=200)
        context = {
            'website_id': str(wid),
            'page_id': request.GET.get('page_id'),
            'page': request.GET.get('page'),
            'slug': request.GET.get('slug'),
            'title': request.GET.get('title'),
            'tags': request.GET.get('tags'),
            'categories': request.GET.get('categories'),
            'keywords': request.GET.get('keywords'),
            'content': request.GET.get('content'),
            'description': request.GET.get('description'),
            'in_navbar': request.GET.get('in_navbar'),
            'date_published': request.GET.get('date_published')
        }
        return render(request, 'hugo_v2/partials/site-update-page-form.html', context)
    except Exception as e:
        print(e)


def cancel_page(request, pk):
    return render(request, 'hugo_v2/partials/site-add-page-form.html', {'website_id': str(pk)})


def delete_page(request, wid, pk):
    token = get_token(request)
    req = requests.post(f"http://127.0.0.1:7000/api/delete-page-v2/{wid}/{pk}/", headers={'Authorization': f'Bearer {token}'})
    if req.status_code == 200 or req.status_code == 201:
        return render(request, 'hugo_v2/partials/site-add-page-form.html', {'website_id': str(wid)})