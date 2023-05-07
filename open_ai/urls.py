from django.urls import path, include
from .views import user_open_ai, user_open_ai_logs, user_open_ai_content_view, create_generate_content, \
    GenerateIntroduction, GenerateFirstSection, GenerateOtherSections, GenerateConclusion, user_open_ai_assisted_gc, \
    user_open_ai_assisted_gc_generate_headers, GenerateFirstSectionAndOtherSections, user_open_ai_content_view_headers, \
    user_open_ai_assisted_gc_view_results, user_open_ai_prompt, user_open_ai_prompt_update, user_open_ai_view_logs, \
    user_open_ai_prompt_parent, user_open_ai_prompt_parent_view, user_open_ai_assisted_gc_view_prompt


urlpatterns = [
    path('content/generator/', user_open_ai, name='user_open_ai'),
    path('prompt/parent/', user_open_ai_prompt_parent, name='user_open_ai_prompt_parent'),
    path('prompt/parent/view/<int:pk>/', user_open_ai_prompt_parent_view, name='user_open_ai_prompt_parent_view'),
    path('prompt/', user_open_ai_prompt, name='user_open_ai_prompt'),
    path('prompt/view/<int:pk>/', user_open_ai_prompt_update, name='user_open_ai_prompt_update'),
    path('content/introduction/<str:keyword>/<str:headers>', GenerateIntroduction, name='introduction'),
    path('content/sections/first/<str:keyword>/<str:title>', GenerateFirstSection, name='first_section'),
    path('content/sections/others/<str:keyword>/<str:title>/<str:previous_title>',
         GenerateOtherSections, name='other_sections'),
    path('content/conclusion/<str:keyword>/<str:headers>', GenerateConclusion, name='conclusion'),
    path('content/generator/logs/', user_open_ai_logs, name='user_open_ai_logs'),
    path('content/generator/view-logs/<int:pk>/', user_open_ai_view_logs, name='user_open_ai_view_logs'),
    path('create_generate_content/', create_generate_content, name='create_generate_content'),
    path('user_open_ai_content_view/<int:pk>/', user_open_ai_content_view, name='user_user_open_ai_content_viewopen_ai_logs'),
    path('assisted/gc/', user_open_ai_assisted_gc, name='user_open_ai_assisted_gc'),
    path('assisted/gc/view/<int:pk>/', user_open_ai_assisted_gc_view_prompt, name='user_open_ai_assisted_gc_view_prompt'),
    path('assisted/gc/generate_headers/', user_open_ai_assisted_gc_generate_headers, name='user_open_ai_assisted_gc_generate_headers'),
    path('GenerateFirstSectionAndOtherSections/', GenerateFirstSectionAndOtherSections, name='GenerateFirstSectionAndOtherSections'),
    path('user_open_ai_content_view_headers/<int:pk>/', user_open_ai_content_view_headers, name='user_open_ai_content_view_headers'),
    path('user_open_ai_assisted_gc_view_results/<int:pk>/', user_open_ai_assisted_gc_view_results, name='user_open_ai_assisted_gc_view_results'),
]