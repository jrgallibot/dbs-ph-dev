from django.urls import path, include
from . views import *


urlpatterns = [
    path('', index_page),
    path('add-website/', add_website_page),
    path('website/<slug:pk>/', website_page),
    path('publish-website/<slug:wid>/', publish_website_page),
    path('add-page/<slug:pk>/', add_page),
    path('update-page/<slug:wid>/', update_page),
    path('cancel-page/<slug:pk>/', cancel_page),
    path('delete-page/<slug:wid>/<slug:pk>/', delete_page)
]
