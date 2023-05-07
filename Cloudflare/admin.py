from django.contrib import admin

# Register your models here.
from .models import CloudflareModel,CloudflareDNS

from indexer.admin import indexer_admin_site

class AutoChooseUser(admin.ModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
# Register your models here.

indexer_admin_site.register(CloudflareModel,AutoChooseUser)
indexer_admin_site.register(CloudflareDNS)