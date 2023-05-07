from django.urls import path

from . views import IndexApiListView, IndexApiDetailView, IndexWebsitesListView, IndexWebPagesDetailView, \
    LogsView, UsageIndexListView, IndexApiTypeMethodView, MobileFriendlyListView, MobileFriendlyPagesView, \
    IndexApiTypeDetailView, UserIndexApiListView, UserIndexWebsitesListView, UserIndexWebPagesDetailView, UserMobileFriendlyListView, \
    UserMobileFriendlyPagesView, UserSiteMapListView, UserSiteMapPagesView, ListofusersView, RankSearchListView, SiteMapListView, RankTrackerHistoryCostView, \
    RankSearchOverALlTotalCostListView, ImageOptimizerListView, ImageOptimizerFileView, OpenAiContentListView, OpenAiAssistedGCListView, \
    OpenAiAssistedGCHeadersListView, OpenAiPromptListView, OpenAiPromptParentListView, CloudflareModelListView, CloudflareModelUrllListView

urlpatterns = [
    path('list/', IndexApiListView.as_view(), name='api-all'),
    path('api/type/method/', IndexApiTypeMethodView.as_view(), name='api-type-method'),
    path('detail/<int:pk>', IndexApiDetailView.as_view(), name='api-detail'),
    path('type/detail/<int:pk>', IndexApiTypeDetailView.as_view(), name='api-type-detail'),
    path('list/websites/', IndexWebsitesListView.as_view(), name='api-websites-index'),
    path('website/pages/detail/<int:pk>', IndexWebPagesDetailView.as_view(), name='api-website-pages-detail'),
    path('logs/', LogsView.as_view(), name='api_logs'),
    path('index-usage/<int:pk>', UsageIndexListView.as_view(), name='api_index_usage'),
    path('sitemap/', SiteMapListView.as_view(), name='api_site_map'),

    # CLOUD FLARE
    path('user/cloudflare/api/<int:pk>', CloudflareModelListView.as_view(), name='api_cloud_flare'),
    path('user/cloudflare/api/sites/<int:pk>', CloudflareModelUrllListView.as_view(), name='api_cloud_flare_sites'),

    # OPEN AI
    path('user/open_ai_content_logs/<int:pk>', OpenAiContentListView.as_view(), name='api_open_ai_content_logs'),
    path('user/open_ai_assisted_gc/<int:pk>', OpenAiAssistedGCListView.as_view(), name='api_open_ai_assisted_gc'),
    path('user/open_ai_assisted_gc_headers/<int:pk>', OpenAiAssistedGCHeadersListView.as_view(), name='api_open_ai_assisted_gc_headers'),
    path('user/open_ai_prompt/', OpenAiPromptListView.as_view(), name='api_open_ai_prompt'),
    path('user/open_ai_prompt_parent/', OpenAiPromptParentListView.as_view(), name='api_open_ai_prompt_parent'),

    #MOBILE FRIENDLY API URL
    path('mobile_friendly/', MobileFriendlyListView.as_view(), name='api_mobile_friendly'),
    path('mobile_friendly/website/pages/detail/<int:pk>', MobileFriendlyPagesView.as_view(), name='api-mobilefriendly-website-pages'),

    path('user/api/list-of-users/', ListofusersView.as_view(), name='api-listofusers'),
    path('rank-search/<int:pk>', RankSearchListView.as_view(), name='api-rank-search'),
    path('rank-search/history/<int:pk>', RankTrackerHistoryCostView.as_view(), name='api-rank-search-history'),
    path('rank-tracker-cost/', RankSearchOverALlTotalCostListView.as_view(), name='api-rank-tracker-cost'),

    # ImageOptimizer
    path('image-optimizer/<int:pk>', ImageOptimizerListView.as_view(), name='api-image-optimizer'),
    path('image-optimizer-file/<int:pk>', ImageOptimizerFileView.as_view(), name='api-image-optimizer-file'),

    #USER SIDE
    path('user/api/list/<int:pk>', UserIndexApiListView.as_view(), name='api-user'),
    path('user/website/list/<int:pk>', UserIndexWebsitesListView.as_view(), name='api-user-website-list'),
    path('user/website/pages/detail/<int:pk>', UserIndexWebPagesDetailView.as_view(), name='api-user-website-pages-detail'),
    path('mobile/friendly/<int:pk>', UserMobileFriendlyListView.as_view(), name='api_user_mobile_friendly'),
    path('user/mobile/friendly/website/pages/detail/<int:pk>', UserMobileFriendlyPagesView.as_view(), name='api-user-mobilefriendly-website-pages'),
    path('site-map/<int:pk>', UserSiteMapListView.as_view(), name='api_user_site_map'),
    path('site-map/pages/<int:pk>', UserSiteMapPagesView.as_view(), name='api_user_site_map_pages'),
]