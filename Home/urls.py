"""Indexer App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from rest_framework.documentation import include_docs_urls, get_schemajs_view

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.contrib.sitemaps import Sitemap
from wagtail.documents import urls as wagtaildocs_urls


from apps.teams.urls import team_urlpatterns as single_team_urls
from apps.subscriptions.urls import team_urlpatterns as subscriptions_team_urls
from apps.web.urls import team_urlpatterns as web_team_urls
from apps.web.sitemaps import StaticViewSitemap
from Home.sitemaps import IndexerSitemap
from indexer.admin import indexer_admin_site
from ckeditor_uploader.views import upload

PagesAPIViewSet.schema = None  # hacky workaround for https://github.com/wagtail/wagtail/issues/8583
schemajs_view = get_schemajs_view(title="API")

sitemaps = {
    'indexer': IndexerSitemap,
    # 'static':StaticSitemap
}

# urls that are unique to using a team should go here
team_urlpatterns = [
    path('', include(web_team_urls)),
    path('subscription/', include(subscriptions_team_urls)),
    path('team/', include(single_team_urls)),
    path('example/', include('apps.teams_example.urls')),
]

urlpatterns = [
    path('portal/', indexer_admin_site.urls),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap.xml', sitemap, {'sitemaps': {'indexer' : IndexerSitemap}},name='django.contrib.sitemaps.views.sitemap'),
    path('a/<slug:team_slug>/', include(team_urlpatterns)),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls')),
    path('hugo-client/', include('client.urls')),
    path('hugo-client-v2/', include('hugo_client_v2.urls')),
    path('cloudflare/', include('Cloudflare.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
    path('teams/', include('apps.teams.urls')),
    path('', include('apps.web.urls')),
    path('pegasus/', include('pegasus.apps.examples.urls')),
    path('indexer/', include('indexer.urls')),
    path("indexer/user/", include('indexer.user_side.urls')),
    path('mobile-friendly/', include('mobile_friendly.urls')),
    path('indexer/user/image-optimizer/', include('image_optimizer.urls')),
    path('user/open-ai/', include('open_ai.urls')),
    path('pegasus/employees/', include('pegasus.apps.employees.urls')),
    path('celery-progress/', include('celery_progress.urls')),
    # API docs
    # these are needed for schema.js
    path('docs/', include_docs_urls(title='API Docs')),
    path('schemajs/', schemajs_view, name='api_schemajs'),
    # djstripe urls - for webhooks
    path("stripe/", include("djstripe.urls", namespace="djstripe")),

    # wagtail config
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('content/', include(wagtail_urls)),
    path('ckeditor/', upload, name='ckeditor_upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'dashboard.views.page_not_found'