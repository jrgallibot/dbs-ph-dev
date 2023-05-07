from django.contrib import sitemaps
from django.urls import reverse
from indexer.models import *
from mobile_friendly.models import *

class IndexerSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'
    
    def items(self):
        return Website.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    # def location(self, obj):
    #     return obj.get_absolute_url

    def location(self, obj):
        return f'/{obj.id}'


# class StaticSitemap(sitemaps.Sitemap):
#     changefreq = "yearly"
#     priority = 0.8
#     protocol = 'https'

#     def items(self):
#         return ['main:homepage_view', 'main:contact_view']

#     def location(self, item):
#         return reverse(item)