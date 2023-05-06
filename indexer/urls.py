from django.urls import path, include
from .views import IndexApiListView, IndexApiDetailView, IndexApiCreateView, WebsiteListView, \
    WebsiteDetailView, WebsiteCreateView, IndexApiUpdateView, WebsiteUpdateView, SitemapCreateView, SitemapListView, \
    SitemapUpdateView, indexing
from . import views

app_name = 'indexer_app'

urlpatterns = [
    # new urls
    path("new/", include('indexer.new.urls')),

    # old urls
    path("", IndexApiListView.as_view(), name='IndexApilist'),
    path("<int:pk>/", IndexApiDetailView.as_view(), name='IndexApidetail'),
    path("add/", IndexApiCreateView.as_view(), name='indexer'),
    path("edit/<int:pk>/", IndexApiUpdateView.as_view(), name='indexerupdate'),
    path("pages/", WebsiteListView.as_view(), ),
    path("pages/<int:pk>/", WebsiteDetailView.as_view(), name='websitedetail'),
    path("pages/add/", WebsiteCreateView.as_view(), name='website'),
    path("pages/edit/<int:pk>/", WebsiteUpdateView.as_view(), name='websiteupdate'),
    path("sitemap/", SitemapListView.as_view(), name='sitemaplist'),
    path("sitemap/add/", SitemapCreateView.as_view(), name='sitemap'),
    path("sitemap/edit/<int:pk>/", SitemapUpdateView.as_view(), name='sitemapupdate'),
]
