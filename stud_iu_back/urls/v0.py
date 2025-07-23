from django.urls import include, path


urlpatterns = [
    path('partners/', include('partners.urls')),
    path('board_members/', include('board_members.urls')),
    path('events/', include('events.urls')),
]
