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


"""def maintenance_mode_enabled():
    data = MaintenanceStatus.objects.filter(Q(id = 1) & Q(name = 'pbn')).first()
    return True if data.status == 0 else False


def maintenance_mode(original_function):
    def wrapper(*args, **kwargs):
        # Check if maintenance mode is enabled
        if maintenance_mode_enabled():
            # Handle maintenance mode logic
            print("Service is currently under maintenance. Please try again later.")
            return HttpResponse("Service is currently under maintenance. Please try again later.")
        else:
            # Execute the original function
            return original_function(*args, **kwargs)
    
    return wrapper"""

def get_token(request):
    client_settings = ClientSettings.objects.get(user=request.user)
    return client_settings.access_token


@login_required
def index_page(request):
    try:
        token = get_token(request)
        group_pbn = ClientPbnGroup.objects.filter(status=1, user_id=request.user.id).all()
        context = {'title': 'Hugo Client', 'module_name': 'Hugo', 'group_pbn': group_pbn,
                   'data': requests.get("http://127.0.0.1:7000/api/home-page-v2/",
                                        headers={'Authorization': f'Bearer {token}'}).json(), 'active_tab': 'hugo_v2'}

        return render(request, 'hugo_v2/index.html', context)
    except Exception as e:
        print(e)


@login_required
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
        if req.status_code == 200 or req.status_code == 201:
            return redirect('/hugo-client-v2/')
    except Exception as e:
        print(e)


@login_required
def website_page(request, pk):
    try:
        token = get_token(request)
        data = requests.get(f"http://127.0.0.1:7000/api/site-page-v2/{pk}/",
                                                   headers={'Authorization': f'Bearer {token}'}).json()

        if str(pk) not in request.session:
            request.session[str(pk)] = requests.get(f"http://127.0.0.1:7000/api/site-page-v2/{pk}/",
                                                   headers={'Authorization': f'Bearer {token}'}).json()
            request.session.save()
        print(request.session.get(str))
        context = {
            'title': 'Hugo Client', 
            'module_name': 'Hugo',
            'website_id': str(pk),
            'data': request.session.get(str(pk)),
            'cloudflare': CloudflareModel.objects.filter(user=request.user).all(),
            'cl_comments': ClientComments.objects.filter(user_id=request.user.id, web_id=pk).all(),
            'group_pbn': ClientPbnGroup.objects.filter(status=1, user_id=request.user.id).all()
        }
        return render(request, 'hugo_v2/partials/site.html', context)
    except Exception as e:
        print(e)


@login_required
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
            'tags': request.POST.getlist('tags[]'),
            'categories': request.POST.getlist('categories[]'),
            'keywords': request.POST.getlist('keywords[]'),
            'in_navbar': True if request.POST.get('in_navbar') == "on" else False,
        }
        req = requests.post(f"http://127.0.0.1:7000/api/add-page-v2/",
                            headers={'Authorization': f'Bearer {token}'}, json=data)
        
        temp_sites = None
        if str(pk) not in request.session:
            temp_sites = req.json()
        else:
            temp_sites = request.session.get(str(pk))['website']['pages']
            temp_sites.append(req.json())

        request.session[str(pk)]['website']['pages'] = temp_sites
        request.session.save()


        if req.status_code == 200 or req.status_code == 201:
            return JsonResponse({'data': req.text, 'website_id': str(pk)}, status=200)
        else:
            return JsonResponse({'statusMsg': req.text}, status=404)
    except Exception as e:
        print(e) 


@login_required
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

        req = requests.post(
            f"http://127.0.0.1:7000/api/publish-website-v2/{wid}/",
            headers={'Authorization': f'Bearer {token}'}, data=data)
    
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
            context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
            messages.error(request, req.json()['statusMsg'])
            return render(request, 'hugo_v2/partials/site-cloudflare-details-card.html', context)
    except Exception as e:
        print(e)
        return JsonResponse({'statusMsg': str(e)}, status=404)


@login_required
def update_page(request, wid):
    if request.method == "POST":
        try:
            if request.POST.get('page')[0] != '/' or request.POST.get('page')[-1] != '/':
                return JsonResponse({'statusMsg': 'Invalid Directory.'}, status=404)
            token = get_token(request)
            data = {   
                'website': str(wid),
                'page_id': request.POST.get('page_id'),
                'page': request.POST.get('page'),
                'slug': request.POST.get('slug'),
                'title': request.POST.get('title'),
                'tags': request.POST.getlist('tags[]'),
                'categories': request.POST.getlist('categories[]'),
                'keywords': request.POST.getlist('keywords[]'),
                'content': request.POST.get('content'),
                'description': request.POST.get('description'),
                'in_navbar': request.POST.get('in_navbar') == "on",
                'date_published': request.POST.get('date_published')
            }
            req = requests.post(
                f"http://127.0.0.1:7000/api/update-page-v2/{str(wid)}/{request.POST.get('page_id')}/",
                headers={'Authorization': f'Bearer {token}'},
                json=data
            )
            if req.status_code in {200, 201}:
                for row in request.session.get(str(wid))['website']['pages']:
                    if row['id'] == request.POST.get('page_id'):
                        row.update({   
                            'website': str(wid),
                            'page_id': request.POST.get('page_id'),
                            'page': request.POST.get('page'),
                            'slug': request.POST.get('slug'),
                            'title': request.POST.get('title'),
                            'tags': request.POST.getlist('tags[]'),
                            'categories': request.POST.getlist('categories[]'),
                            'keywords': request.POST.getlist('keywords[]'),
                            'content': request.POST.get('content'),
                            'description': request.POST.get('description'),
                            'in_navbar': request.POST.get('in_navbar') == "on",
                            'date_published': request.POST.get('date_published')
                        })
                        request.session.modified = True
                        break
                return JsonResponse({'data': req.text, 'website_id': str(wid)}, status=200)
        except Exception as e:
            print(e)

    data = None
    for row in request.session.get(str(wid), [])['website']['pages']:
        if row['id'] == request.GET.get('page_id'):
            row.update({'website_id': str(wid)})
            data = row
            break  # Break out of the loop when a match is found
    return render(request, 'hugo_v2/partials/site-update-page-form.html', data)



@login_required
def cancel_page(request, pk):
    return render(request, 'hugo_v2/partials/site-add-page-form.html', {'website_id': str(pk)})



@login_required
def delete_page(request, wid, pk):
    try:
        token = get_token(request)
        req = requests.post(f"http://127.0.0.1:7000/api/delete-page-v2/{wid}/{pk}/", headers={'Authorization': f'Bearer {token}'})
        if req.status_code == 200 or req.status_code == 201:
            return render(request, 'hugo_v2/partials/site-add-page-form.html', {'website_id': str(wid)})
    except Exception as e:
        print(e)


@require_POST
def page_comments(request, pk):
    if request.method == "POST":
        context = {}
        try:
            comments = ClientComments(
                client_site = request.POST.get('client_site'),
                comments = request.POST.get('notes'),
                user_id = request.user.id,
                web_id = pk
            )
            comments.save()
            messages.success(request, 'You have successfully saved the comments.')
            context['cl_comments'] = ClientComments.objects.filter(user_id=request.user.id, web_id=pk).all()
            return render(request, 'hugo_v2/partials/site-page-comments.html', context)
        except Exception as e:
            print(e)