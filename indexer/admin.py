from django.contrib import admin
from django import forms
from django_celery_results.models import TaskResult, GroupResult

class IndexerAdminSite(admin.AdminSite):
    site_header = "Indexer Quick Portal"
    site_title = "Indexer Admin Portal"
    index_title = "Welcome to Indexer Portal"

class AutoChooseUser(admin.ModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
# Register your models here.
from .models import *

class IndexApiAdminForm(forms.ModelForm):

    class Meta:
        model = IndexApi
        fields = "__all__"

    def save(self,request, commit=True):
        obj = super(IndexApiAdminForm, self).save(commit=False)
        obj.user = request.user # Assigning the object reference
        obj.save()
        return obj


admin.site.register(IndexApi)
admin.site.register(Website)
admin.site.register(GSCVerify)
admin.site.register(UrlShortner)

indexer_admin_site = IndexerAdminSite(name='indexer_admin')

indexer_admin_site.register(IndexApi,AutoChooseUser)
indexer_admin_site.register(Website)
indexer_admin_site.register(GSCVerify,AutoChooseUser)
indexer_admin_site.register(UrlShortner)
indexer_admin_site.register(TaskResult)
indexer_admin_site.register(GroupResult)