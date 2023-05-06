from django.urls import path, include
from .views import cloud_fare_api, cloud_fare_api_view, add_sites, generate_updated_sites, edit_dns, cloud_fare_api_view_sites, \
    edit_dns_record, delete_dns_record, page_rule


urlpatterns = [
    path('user/api', cloud_fare_api, name='cloud_fare_api'),
    path('add_sites/', add_sites, name='add_sites'),
    path('delete_dns_record/', delete_dns_record, name='delete_dns_record'),
    path('generate_updated_sites/', generate_updated_sites, name='generate_updated_sites'),
    path('user/api/view/<int:pk>', cloud_fare_api_view, name='cloud_fare_api_view'),
    path('edit_dns/<int:pk>', edit_dns, name='edit_dns'),
    path('page_rule/<int:pk>', page_rule, name='page_rule'),
    path('edit_dns_record/<str:record_id>/<int:pk>', edit_dns_record, name='edit_dns_record'),
    path('cloud_fare_api_view_sites/<int:pk>', cloud_fare_api_view_sites, name='cloud_fare_api_view_sites'),
]