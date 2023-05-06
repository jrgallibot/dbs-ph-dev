from django.urls import path, include
from .views import user_image_optimizer, download_image_again


urlpatterns = [
    path('', user_image_optimizer, name='image_optimizer'),
    path('download_image_again/<int:pk>', download_image_again, name='download_image_again'),
]
