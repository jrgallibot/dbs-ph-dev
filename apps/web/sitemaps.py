from django.contrib import sitemaps
from django.urls import reverse
from indexer.models import *
from mobile_friendly.models import *
from .meta import get_protocol


class StaticViewSitemap(sitemaps.Sitemap):
    """
    Sitemap for serving any static content you want.
    """

    @property
    def protocol(self):
        return get_protocol()

    def items(self):
        # add any urls (by name) for static content you want to appear in your sitemap to this list
        return [
            'web:home',
        ]

    def location(self, item):
        return reverse(item)



class IndexerSitemap(sitemaps.Sitemap):
    def items(self):
        return Website.objects.all()

    # def location(self, item):
    #     return reverse(item)
