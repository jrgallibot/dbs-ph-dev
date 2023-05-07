from django.urls import path, include
from .views import mobile_friendly_api, mobile_friendly_api_update, check_mobile_friendly_api


urlpatterns = [
    path('', mobile_friendly_api, name='mobile-friendly'),
    path('update/<int:pk>', mobile_friendly_api_update, name='mobile-friendly-update'),
    path('check_mobile_friendly_api/', check_mobile_friendly_api, name='check-mobile-friendly'),
]
