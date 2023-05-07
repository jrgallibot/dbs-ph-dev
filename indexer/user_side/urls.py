from django.urls import path, include
from indexer.user_side.views import user_side_index_api ,user_side_index_api_update, user_indexing_website, user_add_pages, \
    user_update_website_index, user_check_pages, user_dashboard_page, user_mobile_friendly, user_mobile_friendly_update, \
    user_check_mobile_friendly_api, user_site_map, user_site_map_update, user_check_the_sitemap, user_rank_tracker, \
    register_user, view_users, check_sitemap_lastmod_update, website_user_add_pages_not_exist, user_update_rank_tracker, \
    user_google_index_web_delete, user_google_index_pages_delete, user_sitemap_web_delete, user_sitemap_pages_delete, \
    check_api_to_validate, user_check_site_url, check_siteurl_update_page, user_check_the_sitemap_duplicated_delete, generate_client_toker_user, \
    check_all_pages_siteurl_update_page, user_check_all_sitemap_gsc
app_name = 'indexer_user'


urlpatterns = [
    path('dashboard/', user_dashboard_page, name='user_dashboard_page'),
    path('index-api/', user_side_index_api, name='user_side_index_api'),
    path('check_api_to_validate/', check_api_to_validate, name='check_api_to_validate'),
    path('index-api/update/<int:pk>', user_side_index_api_update, name='user_side_index_api_update'),
    path('google-index/', user_indexing_website, name='user_indexing_website'),
    path('user_google_index_web_delete/', user_google_index_web_delete, name='user_google_index_web_delete'),
    path('user_google_index_pages_delete/', user_google_index_pages_delete, name='user_google_index_pages_delete'),
    path('user_sitemap_web_delete/', user_sitemap_web_delete, name='user_sitemap_web_delete'),
    path('user_sitemap_pages_delete/', user_sitemap_pages_delete, name='user_sitemap_pages_delete'),
    path('user_check_the_sitemap_duplicated_delete/', user_check_the_sitemap_duplicated_delete, name='user_check_the_sitemap_duplicated_delete'),
    path('add-pages-indexer/', user_add_pages, name='user_add_pages'),
    path('update-user/web-index/websites/<int:pk>', user_update_website_index, name='user_update_website_index'),
    path('check-web-pages/', user_check_pages, name='user_check_pages'),
    path('mobile/friendly/', user_mobile_friendly, name='user_mobile_friendly'),
    path('mobile/friendly/update/<int:pk>', user_mobile_friendly_update, name='user_mobile_friendly_update'),
    path('check/mobile/friendly/', user_check_mobile_friendly_api, name='user_check_mobile_friendly_api'),
    path('site-map/', user_site_map, name='user_site_map'),
    path('update-site-map/<int:pk>/', user_site_map_update, name='user_site_map'),
    path('check-site-map/', user_check_the_sitemap, name='user_check_the_sitemap'),
    path('check-site-map/lastmod/update/', check_sitemap_lastmod_update, name='check_sitemap_lastmod_update'),
    path('check_siteurl_update_page/', check_siteurl_update_page, name='check_siteurl_update_page'),
    path('check_all_pages_siteurl_update_page/', check_all_pages_siteurl_update_page, name='check_all_pages_siteurl_update_page'),
    path('website_user_add_pages_not_exist/', website_user_add_pages_not_exist, name='website_user_add_pages_not_exist'),
    path('user_check_site_url/', user_check_site_url, name='user_check_site_url'),

    #Rank Tracker
    path('rank-tracker/', user_rank_tracker, name='user_rank_tracker'),
    path('update_rank_tracker/<str:pk>', user_update_rank_tracker, name='user_update_rank_tracker'),
    path('user_check_all_sitemap_gsc/<str:pk>', user_check_all_sitemap_gsc, name='user_check_all_sitemap_gsc'),
    

    #Register User
    path('register/account/', register_user, name='register_user'),
    path('generate_client_toker_user/', generate_client_toker_user, name='generate_client_toker_user'),
    path('list-of-accounts/', view_users, name='view_users'),
]