from django.urls import path, include
from . views import *


urlpatterns = [
    path('', index_page),
    path('<slug:action>/', index_page),
    path('<slug:action>/<slug:pk>/', index_page),
]
