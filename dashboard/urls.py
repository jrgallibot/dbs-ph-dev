from django.urls import path
from . views import dashboard_page, dashboard_index_page, index_api_update, dashboard_indexing_website, update_website_index, \
    dashboard_url_shortener, get_url_shortner_api, dashboard_log_history, check_pages, add_pages, website_add_pages_not_exist, \
    api_type, api_type_update, check_pages_index, check_pages_if_mobile_friendly, admin_site_map, admin_site_map_update, \
    admin_check_sitemap_lastmod_update, admin_check_the_sitemap, admin_register_user, admin_view_users, admin_ranktracker_cost

urlpatterns = [
    path('', dashboard_page, name='dashboard-page'),
    path('api/type', api_type, name='api-type'),
    path('api/type/update', api_type_update, name='api-type-update'),
    path('index/api', dashboard_index_page, name='dashboard-index-page'),
    path('update/index/api/<int:pk>', index_api_update, name='update-index-api'),
    path('index/websites', dashboard_indexing_website, name='index-websites'),
    path('update/index/websites/<int:pk>', update_website_index, name='index-websites-update'),
    path('url/shortners', dashboard_url_shortener, name='url-shortners'),
    path('get/data/url/shortners', get_url_shortner_api, name='get-url-shortner-api'),
    path('check-pages', check_pages, name='check-pages'),
    path('add-pages', add_pages, name='add-pages'),
    path('website_add_pages_not_exist', website_add_pages_not_exist, name='website_add_pages_not_exist'),
    path('logs-history', dashboard_log_history, name='logs-history'),
    path('check_pages_index', check_pages_index, name='check_pages_index'),
    path('check_pages_if_mobile_friendly', check_pages_if_mobile_friendly, name='check_pages_if_mobile_friendly'),
    path('sitemap/', admin_site_map, name='admin_site_map'),
    path('sitemap-update/<int:pk>', admin_site_map_update, name='admin_site_map_update'),
    path('admin_check_sitemap_lastmod_update/', admin_check_sitemap_lastmod_update, name='admin_check_sitemap_lastmod_update'),
    path('admin_check_the_sitemap/', admin_check_the_sitemap, name='admin_check_the_sitemap'),
    path('rank-tracker-cost/monitor/', admin_ranktracker_cost, name='admin_ranktracker_cost'),

    # User Management URL's
    path('admin/register-users', admin_register_user, name='admin_register_user'),
    path('admin/list-of-users', admin_view_users, name='admin_view_users'),
]