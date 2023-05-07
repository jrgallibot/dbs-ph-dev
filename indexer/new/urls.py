from django.urls import path, include
from . views import *


urlpatterns = [
    path('', index_page, name='indexer-new-index'),
    path('api/', include('indexer.new.api.urls'))
]