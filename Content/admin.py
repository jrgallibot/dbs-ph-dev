from django.contrib import admin
# Register your models here.
from indexer.admin import indexer_admin_site
from .models import Spintax7 , Yacss,KeywordIdeas


class AutoChooseUser(admin.ModelAdmin):
    exclude = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

class AutoChooseUserSpintax(AutoChooseUser):
    exclude = ('user','content3','content4','content5','content6','content7',)


indexer_admin_site.register(Spintax7,AutoChooseUserSpintax)
indexer_admin_site.register(Yacss,AutoChooseUser)
indexer_admin_site.register(KeywordIdeas,AutoChooseUser)
# Register your models here.
