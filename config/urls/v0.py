from django.urls import include, path

urlpatterns = [
    path('board_members/', include('apps.board_members.urls')),
    path('events/', include('apps.events.urls')),
    path('news/', include('apps.news.urls')),
    path('partners/', include('apps.partners.urls')),
]
