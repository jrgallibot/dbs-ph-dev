from django.http import JsonResponse
from django.shortcuts import render, redirect
from . models import ClientSettings, CloudflareWebsites
import requests
from Cloudflare.models import CloudflareModel
from django.utils.text import slugify
from datetime import datetime, timedelta

def index_page(request, action=None, pk=None):
    try:
        client_settings = ClientSettings.objects.get(user=request.user)
        token = client_settings.access_token
        context = {
            'title': 'Hugo Client',
            'module_name': 'Hugo',
            'data': None
        }
        if client_settings.access_token:
            if action is not None and pk is None:
                if action == "create-hugo-account":
                    data = {
                        'username': 'admin1',
                        'password': 'admin123!'
                    }
                    req = requests.post("http://95.217.184.122/api/token/", json=data)
                elif action == "add-website" and request.method == "POST":
                    data = {
                        'title': request.POST.get('title'),
                        'base_url': request.POST.get('base_url'),
                        'language_code': request.POST.get('language_code'),
                        'theme': request.POST.get('theme'),
                    }
                    req = requests.post("http://95.217.184.122/api/website/", headers={'Authorization': f'Bearer {token}'}, json=data)
                    if req.status_code == 200 or req.status_code == 201:
                        return redirect('/hugo-client/')

                elif action == "add-account" and request.method == "POST":
                    try:
                        check = CloudflareModel.objects.filter(account_token = request.POST.get('token'))
                        cl = CloudflareModel.objects.get(pk = request.POST.get('cloudflare'))
                        if not check:
                            data = {
                                'email': cl.email,
                                'account_id': request.POST.get('id'),
                                'account_token': request.POST.get('token'),
                                'api_key': cl.key,
                                'page_name': None,
                            }
                            CloudflareModel.objects.filter(id=request.POST.get('cloudflare')).update(
                                account_id = data['account_id'],
                                account_token = data['account_token'],
                                status = 1
                            )
                            check_cl_web = CloudflareWebsites.objects.filter(cloudfare_id = request.POST.get('cloudflare'))
                            if not check_cl_web:
                                CloudflareWebsites.objects.create(
                                    cloudfare_id = request.POST.get('cloudflare')
                                )
                            req = requests.post("http://95.217.184.122/api/cloudflare/", headers={'Authorization': f'Bearer {token}'},
                                        json=data)
                            if req.status_code == 200 or req.status_code == 201:
                                return redirect('/hugo-client/')
                        else:
                            return JsonResponse({'statusMsg': 'Account Token duplicated.'}, status=404)
                    except Exception as e:
                        return JsonResponse({'statusMsg': str(e)}, status=404)
                elif action == "cloudflare":
                    data = requests.get("http://95.217.184.122/api/cloudflare/", headers={'Authorization': f'Bearer {token}'})
                    context['data'] = data.json()
                    return render(request, 'indexer-user/hugo/partials/cloudflares.html', context)

                elif action == "website":
                    context['data'] = requests.get("http://95.217.184.122/api/websites/", headers={'Authorization': f'Bearer {token}'}).json()
                    context['themes'] = requests.get("http://95.217.184.122/api/themes/", headers={'Authorization': f'Bearer {token}'}).json()
                    context['cloudflares'] = requests.get("http://95.217.184.122/api/cloudflare/", headers={'Authorization': f'Bearer {token}'}).json()
                    context['cloudflare_model'] = CloudflareModel.objects.filter(status=1)
                    return render(request, 'indexer-user/hugo/partials/sites.html', context)

            elif action is not None and pk is not None:
                if action == "build-website" and request.method == "GET":
                    req = requests.post(f"http://95.217.184.122/api/build-website/{pk}/", headers={'Authorization': f'Bearer {token}'})
                    if req.status_code == 200:
                        return redirect('/hugo-client/')
                elif action == "publish-website" and request.method == "POST":
                    try:
                        req = requests.post(f"http://95.217.184.122/api/publish-website/{pk}/{request.POST.get('cloudflare_id')}/", headers={'Authorization': f'Bearer {token}'})
                        cl_model = CloudflareModel.objects.filter(email = request.POST.get('cloudflare_id')).first()
                        CloudflareWebsites.objects.filter(cloudfare_id = cl_model.id).update(
                            page_name = slugify(request.POST.get('title'))
                        )
                        print('slug', slugify(request.POST.get('title')))
                        print(req.text)
                        if req.status_code == 200 or req.status_code == 201:
                            return JsonResponse({'statusMsg': 'Success'}, status=200)
                    except Exception as e:
                        return JsonResponse({'statusMsg': str(e)}, status=404)
                    return JsonResponse({'statusMsg': 'Internal Server Error'}, status=404)
                elif action == "routes":
                    if request.method == "GET":
                        routes = requests.get(f"http://95.217.184.122/api/website-routes/{pk}/", headers={'Authorization': f'Bearer {token}'})
                        context['data'] = routes.json()
                        context['website_id'] = pk
                        return render(request, 'indexer-user/hugo/partials/routes-modal-content.html', context)
                    elif request.method == "POST":
                        data = {
                            'website': pk,
                            'name': request.POST.get('route_name'),
                            'in_navbar': True if request.POST.get('in_navbar') == "on" else False,
                            'has_pages': True if request.POST.get('has_pages') == "on" else False,
                        }
                        req = requests.post("http://95.217.184.122/api/route/",
                                            headers={'Authorization': f'Bearer {token}'}, json=data)
                        if req.status_code == 200 or req.status_code == 201:
                            routes = requests.get(f"http://95.217.184.122/api/website-routes/{pk}/",
                                                headers={'Authorization': f'Bearer {token}'})
                            context['data'] = routes.json()
                            context['website_id'] = pk
                            return render(request, 'indexer-user/hugo/partials/routes-modal-content.html', context)
                        else:
                            return JsonResponse({'statusMsg': req.text}, status=404)

                elif action == "route-contents":
                    route = requests.get(f"http://95.217.184.122/api/routes/{pk}/",
                                        headers={'Authorization': f'Bearer {token}'})
                    context['route'] = route.json()
                    if request.method == "GET":
                        contents = requests.get(f"http://95.217.184.122/api/route-contents/{pk}/",
                                            headers={'Authorization': f'Bearer {token}'})
                        context['data'] = contents.json()
                        return render(request, 'indexer-user/hugo/partials/routes-contents-modal-content.html', context)
                    elif request.method == "POST":
                        data = {
                            'route': pk,
                            'title': request.POST.get('title'),
                            'content': ''
                        }
                        req = requests.post(f"http://95.217.184.122/api/content/",
                                        headers={'Authorization': f'Bearer {token}'}, data=data)

                        if req.status_code == 200 or req.status_code == 201:
                            contents = requests.get(f"http://95.217.184.122/api/route-contents/{pk}/",
                                                    headers={'Authorization': f'Bearer {token}'})
                            context['data'] = contents.json()
                            return render(request, 'indexer-user/hugo/partials/routes-contents-modal-content.html', context)
                        else:
                            return JsonResponse({'statusMsg': req.text}, status=404)

                elif action == "route-content":
                    if request.method == "GET":
                        content = requests.get(f"http://95.217.184.122/api/contents/{pk}/",
                                            headers={'Authorization': f'Bearer {token}'})
                        context['data'] = content.json()
                        context['content_id'] = pk
                        return render(request, 'indexer-user/hugo/partials/route-content-modal-content.html', context)

                    elif request.method == "POST":
                        data = {
                            'title': request.POST.get('title'),
                            'content': request.POST.get('content')
                        }
                        req = requests.post(f"http://95.217.184.122/api/update-content/{pk}/",
                                            headers={'Authorization': f'Bearer {token}'}, json=data)
                        if req.status_code == 200 or req.status_code == 201:
                            return JsonResponse({'statusMsg': 'Content successfully updated.'}, status=200)
                        else:
                            return JsonResponse({'statusMsg': req.text}, status=404)

                elif action == "update-cloudflare":
                    if request.method == "GET":
                        content = requests.get(f"http://95.217.184.122/api/cloudflare/{pk}/",
                                            headers={'Authorization': f'Bearer {token}'})
                        context['data'] = content.json()
                        context['content_id'] = pk
                        context['cloudflare_model'] = CloudflareModel.objects.filter(status = 1)
                        return render(request, 'indexer-user/hugo/partials/cloudflare-modal-content.html', context)
                    elif request.method == "POST":
                        try:
                            data = {
                                'email': request.POST.get('email'),
                                'account_id': request.POST.get('id'),
                                'account_token': request.POST.get('token'),
                                'api_key': request.POST.get('api_key'),
                                'page_name': None,
                            }
                            check = CloudflareModel.objects.filter(account_token = request.POST.get('token')).first()
                            if check:
                                check.account_id = data['account_id']
                                check.account_token = data['account_token']
                                check.email = data['email']
                                check.key = data['api_key']
                                check.updated_at = datetime.now()
                                check_cl_web = CloudflareWebsites.objects.filter(cloudfare_id = check.id)
                                if not check_cl_web:
                                    CloudflareWebsites.objects.create(
                                        cloudfare_id = check.id)
                            else:
                                create_clf = CloudflareModel.objects.create(
                                    email = data['email'],
                                    key = data['api_key'],
                                    account_id = data['account_id'],
                                    account_token = data['account_token'],
                                    user_id = request.user.id,
                                    status = 1
                                )
                                check_cl_web = CloudflareWebsites.objects.filter(cloudfare_id = create_clf.id)
                                if not check_cl_web:
                                    CloudflareWebsites.objects.create(
                                        cloudfare_id = create_clf.id)
                            account = requests.post(f"http://95.217.184.122/api/cloudflare/{pk}/",
                                                headers={'Authorization': f'Bearer {token}'}, json=data)
                            context['data'] = account.json()
                            return render(request, 'indexer-user/hugo/partials/cloudflare-modal-content.html', context)
                        except Exception as e:
                            return JsonResponse({'statusMsg': str(e)}, status=404)
                        
            context['data'] = requests.get("http://95.217.184.122/api/websites/",
                                        headers={'Authorization': f'Bearer {token}'}).json()
            context['themes'] = requests.get("http://95.217.184.122/api/themes/",
                                            headers={'Authorization': f'Bearer {token}'}).json()
            context['cloudflares'] = requests.get("http://95.217.184.122/api/cloudflare/",
                                                headers={'Authorization': f'Bearer {token}'}).json()
            context['cloudflare_model'] = CloudflareModel.objects.filter(status = 1)
            context['active_tab'] = 'hugo'
            return render(request, 'indexer-user/hugo/index.html', context)
        else:
            context['active_tab'] = 'hugo'
            return render(request, 'indexer-user/hugo/index.html', context)
    except Exception as e:
        print(e)