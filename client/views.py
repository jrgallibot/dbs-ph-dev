from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . models import ClientSettings, CloudflareWebsites
from Cloudflare.models import CloudflareModel
from datetime import datetime
import requests


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
                        'description': request.POST.get('description')
                    }
                    req = requests.post("http://95.217.184.122/api/website/",
                                        headers={'Authorization': f'Bearer {token}'}, json=data)
                    if req.status_code == 200 or req.status_code == 201:
                        return redirect('/hugo-client/')

                elif action == "add-account" and request.method == "POST":
                    try:
                        check = CloudflareModel.objects.filter(account_token=request.POST.get('token'))
                        cl = CloudflareModel.objects.get(pk=request.POST.get('cloudflare'))
                        if not check:
                            data = {
                                'email': cl.email,
                                'account_id': request.POST.get('id'),
                                'account_token': request.POST.get('token'),
                                'api_key': cl.key,
                                'page_name': None,
                            }
                            CloudflareModel.objects.filter(id=request.POST.get('cloudflare')).update(
                                account_id=data['account_id'],
                                account_token=data['account_token'],
                                status=1
                            )
                            check_cl_web = CloudflareWebsites.objects.filter(
                                cloudfare_id=request.POST.get('cloudflare'))
                            if not check_cl_web:
                                CloudflareWebsites.objects.create(
                                    cloudfare_id=request.POST.get('cloudflare')
                                )
                            req = requests.post("http://95.217.184.122/api/cloudflare/",
                                                headers={'Authorization': f'Bearer {token}'},
                                                json=data)
                            if req.status_code == 200 or req.status_code == 201:
                                return redirect('/hugo-client/')
                        else:
                            return JsonResponse({'statusMsg': 'Account Token duplicated.'}, status=404)
                    except Exception as e:
                        return JsonResponse({'statusMsg': str(e)}, status=404)

                elif action == "cloudflare":
                    data = requests.get("http://95.217.184.122/api/cloudflare/",
                                        headers={'Authorization': f'Bearer {token}'})
                    context['data'] = data.json()
                    return render(request, 'indexer-user/hugo/partials/cloudflares.html', context)

                elif action == "websites":
                    context['data'] = requests.get("http://95.217.184.122/api/home-page/",
                                                   headers={'Authorization': f'Bearer {token}'}).json()
                    context['active_tab'] = 'hugo'
                    return render(request, 'indexer-user/hugo/partials/sites.html', context)

            elif action is not None and pk is not None:
                if action == "update-website" and request.method == "POST":
                    data = {
                        'id': pk,
                        'title': request.POST.get('title'),
                        'base_url': request.POST.get('base_url'),
                        'language_code': request.POST.get('language_code'),
                        'theme': request.POST.get('theme'),
                        'description': request.POST.get('description')
                    }
                    req = requests.post(
                        f"http://95.217.184.122/api/update-website/{pk}/",
                        headers={'Authorization': f'Bearer {token}'}, data=data)
                    if req.status_code == 200 or req.status_code == 201:
                        messages.success(request, 'You have successfully updated the website.')
                        context['data'] = requests.get(f"http://95.217.184.122/api/site-page/{pk}/",
                                                       headers={'Authorization': f'Bearer {token}'}).json()
                        context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
                        return render(request, 'indexer-user/hugo/partials/site-details-card.html', context)
                    else:
                        context['data'] = requests.get(f"http://95.217.184.122/api/site-page/{pk}/",
                                                       headers={'Authorization': f'Bearer {token}'}).json()
                        context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
                        messages.error(request, 'Internal Server Error')
                        return render(request, 'indexer-user/hugo/partials/site-details-card.html', context)
                elif action == "build-website" and request.method == "GET":
                    req = requests.post(f"http://95.217.184.122/api/build-website/{pk}/",
                                        headers={'Authorization': f'Bearer {token}'})
                    if req.status_code == 200:
                        return redirect('/hugo-client/')

                elif action == "publish-website" and request.method == "POST":
                    try:
                        cloudflare = CloudflareModel.objects.get(id=request.POST.get('cloudflare'), user=request.user)
                        data = {
                            'account_id': cloudflare.account_id,
                            'account_token': cloudflare.account_token,
                            'api_key': cloudflare.key,
                            'email': cloudflare.email,
                            'domain': request.POST.get('domain')
                        }
                        req = requests.post(
                            f"http://95.217.184.122/api/publish-website/{pk}/",
                            headers={'Authorization': f'Bearer {token}'}, data=data)
                        if req.status_code == 200 or req.status_code == 201:
                            cfw = CloudflareWebsites.objects.filter(website_id=pk).first()
                            if cfw:
                                cfw.cloudflare = cloudflare
                                cfw.save()
                            else:
                                CloudflareWebsites.objects.create(website_id=pk, cloudflare=cloudflare)
                            messages.success(request, 'You have successfully published a website.')
                            context['data'] = {
                                'website': requests.get(f"http://95.217.184.122/api/websites/{pk}/",
                                                           headers={'Authorization': f'Bearer {token}'}).json()
                            }
                            context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
                            return render(request, 'indexer-user/hugo/partials/site-cloudflare-details-card.html', context)
                        else:
                            context['data'] = {
                                'website': requests.get(f"http://95.217.184.122/api/websites/{pk}/",
                                                        headers={'Authorization': f'Bearer {token}'}).json()
                            }
                            context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
                            messages.error(request, req.json()['statusMsg'])
                            return render(request, 'indexer-user/hugo/partials/site-cloudflare-details-card.html', context)
                    except Exception as e:
                        return JsonResponse({'statusMsg': str(e)}, status=404)

                elif action == "routes":
                    if request.method == "GET":
                        routes = requests.get(f"http://95.217.184.122/api/website-routes/{pk}/",
                                              headers={'Authorization': f'Bearer {token}'})
                        context['data'] = routes.json()
                        context['website_id'] = pk
                        return render(request, 'indexer-user/hugo/partials/routes-modal-content.html', context)
                    elif request.method == "POST":
                        data = {
                            'website': pk,
                            'name': request.POST.get('route_name'),
                            'in_navbar': True if request.POST.get('in_navbar') == "on" else False,
                            'has_pages': True if request.POST.get('has_pages') == "on" else False,
                            'description': request.POST.get('description')
                        }
                        req = requests.post("http://95.217.184.122/api/route/",
                                            headers={'Authorization': f'Bearer {token}'}, json=data)
                        if req.status_code == 200 or req.status_code == 201:

                            context['data'] = requests.get(f"http://95.217.184.122/api/site-page/{pk}/",
                                                           headers={'Authorization': f'Bearer {token}'}).json()
                            context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
                            messages.success(request, 'Route successfully added.')
                            return render(request, 'indexer-user/hugo/partials/site-page-details-card.html', context)
                        else:
                            context['data'] = requests.get(f"http://95.217.184.122/api/site-page/{pk}/",
                                                           headers={'Authorization': f'Bearer {token}'}).json()
                            context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
                            messages.error(request, 'Invalid/Duplicate Information')
                            return render(request, 'indexer-user/hugo/partials/site-page-details-card.html', context)

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
                            'content': '',
                            'description': request.POST.get('description')
                        }
                        req = requests.post(f"http://95.217.184.122/api/content/",
                                            headers={'Authorization': f'Bearer {token}'}, data=data)

                        if req.status_code == 200 or req.status_code == 201:
                            contents = requests.get(f"http://95.217.184.122/api/route-contents/{pk}/",
                                                    headers={'Authorization': f'Bearer {token}'})
                            context['data'] = contents.json()
                            return render(request, 'indexer-user/hugo/partials/routes-contents-modal-content.html',
                                          context)
                        else:
                            return JsonResponse({'statusMsg': req.text}, status=404)
                elif action == "route-content":
                    if request.method == "GET":
                        routes = requests.get(f"http://95.217.184.122/api/website-routes/{pk}/",
                                              headers={'Authorization': f'Bearer {token}'})
                        context['routes'] = routes.json()
                        context['website_id'] = pk
                        return render(request, 'indexer-user/hugo/partials/site-page-add-content-modal.html', context)

                    elif request.method == "POST":
                        data = {
                            'route': request.POST.get('route'),
                            'title': request.POST.get('title'),
                            'content': request.POST.get('content'),
                            'description': request.POST.get('description')
                        }
                        req = requests.post(f"http://95.217.184.122/api/content/",
                                            headers={'Authorization': f'Bearer {token}'}, json=data)
                        if req.status_code == 200 or req.status_code == 201:
                            return JsonResponse({'statusMsg': 'Content successfully added.'}, status=200)
                        else:
                            return JsonResponse({'statusMsg': req.text}, status=404)

                elif action == "update-route-content":
                    if request.method == "GET":
                        content = requests.get(f"http://95.217.184.122/api/contents/{pk}/",
                                               headers={'Authorization': f'Bearer {token}'})
                        routes = requests.get(f"http://95.217.184.122/api/website-routes/{content.json()['website_id']}/",
                                              headers={'Authorization': f'Bearer {token}'})

                        context['routes'] = routes.json()
                        context['data'] = content.json()
                        context['content_id'] = pk
                        return render(request, 'indexer-user/hugo/partials/site-page-update-content-modal.html', context)

                    elif request.method == "POST":
                        data = {
                            'route': request.POST.get('route'),
                            'title': request.POST.get('title'),
                            'content': request.POST.get('content'),
                            'is_active': True if request.POST.get('is_active') == "on" else False,
                            'description': request.POST.get('description')
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
                        context['cloudflare_model'] = CloudflareModel.objects.filter(status=1)
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
                            check = CloudflareModel.objects.filter(account_token=request.POST.get('token')).first()
                            if check:
                                check.account_id = data['account_id']
                                check.account_token = data['account_token']
                                check.email = data['email']
                                check.key = data['api_key']
                                check.updated_at = datetime.now()
                                check_cl_web = CloudflareWebsites.objects.filter(cloudfare_id=check.id)
                                if not check_cl_web:
                                    CloudflareWebsites.objects.create(
                                        cloudfare_id=check.id)
                            else:
                                create_clf = CloudflareModel.objects.create(
                                    email=data['email'],
                                    key=data['api_key'],
                                    account_id=data['account_id'],
                                    account_token=data['account_token'],
                                    user_id=request.user.id,
                                    status=1
                                )
                                check_cl_web = CloudflareWebsites.objects.filter(cloudfare_id=create_clf.id)
                                if not check_cl_web:
                                    CloudflareWebsites.objects.create(
                                        cloudfare_id=create_clf.id)
                            account = requests.post(f"http://95.217.184.122/api/cloudflare/{pk}/",
                                                    headers={'Authorization': f'Bearer {token}'}, json=data)
                            context['data'] = account.json()
                            return render(request, 'indexer-user/hugo/partials/cloudflare-modal-content.html', context)
                        except Exception as e:
                            return JsonResponse({'statusMsg': str(e)}, status=404)

                elif action == "delete-website":
                    req = requests.post(f"http://95.217.184.122/api/delete-website/{pk}/",
                                           headers={'Authorization': f'Bearer {token}'})
                    context['data'] = requests.get("http://95.217.184.122/api/home-page/",
                                                   headers={'Authorization': f'Bearer {token}'}).json()
                    if req.status_code == 200 or req.status_code == 201:
                        messages.success(request, 'Website Successfully Deleted.')
                        return render(request, 'indexer-user/hugo/partials/sites.html', context)
                    else:
                        messages.error(request, 'Something went wrong.')
                        return render(request, 'indexer-user/hugo/partials/sites.html', context)
                elif action == "website":
                    context['data'] = requests.get(f"http://95.217.184.122/api/site-page/{pk}/",
                                                   headers={'Authorization': f'Bearer {token}'}).json()
                    context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
                    return render(request, 'indexer-user/hugo/partials/site.html', context)
                elif action == "website-view":
                    context['data'] = requests.get("http://95.217.184.122/api/home-page/",
                                                   headers={'Authorization': f'Bearer {token}'}).json()
                    context['cloudflare'] = CloudflareModel.objects.filter(user=request.user).all()
                    return render(request, 'indexer-user/hugo/site-view.html', context)
    
            context['data'] = requests.get("http://95.217.184.122/api/home-page/",
                                           headers={'Authorization': f'Bearer {token}'}).json()
            context['active_tab'] = 'hugo'
            return render(request, 'indexer-user/hugo/index.html', context)
        else:
            context['active_tab'] = 'hugo'
            return render(request, 'indexer-user/hugo/index.html', context)
    except Exception as e:
        print(e)