from django.urls import include, path


urlpatterns = [
    path('board_members/', include('board_members.urls')),
    path('events/', include('events.urls')),
]
