from django.contrib import admin
from .models import Backlinks, Sites , DigitalProperty

class DigitalPropertyClient(DigitalProperty):

    class Meta:
        proxy = True


# Register your models here.
from indexer.admin import indexer_admin_site

class CustomModelAdmin(admin.ModelAdmin):
    
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]

        #if self.list_display.index('user'):
        #    self.list_display.remove('user')

        super(CustomModelAdmin, self).__init__(model, admin_site)

class AutoChooseUser(CustomModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
# Register your models here.

class DigitalPropertyAdmin(admin.ModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    list_display = [
        "domain",
        "status",
        "nameserver",
        "importance",
        "notes",
        "registrar",
        'expireDate'

    ]
    list_filter = ('status', 'importance')
    ordering = ('-updated_at',)
# Register your models here.

indexer_admin_site.register(Backlinks,CustomModelAdmin)
indexer_admin_site.register(Sites,AutoChooseUser)
indexer_admin_site.register(DigitalProperty,DigitalPropertyAdmin)
#indexer_admin_site.register(DigitalPropertyClient,DigitalPropertyAdmin)