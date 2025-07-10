from django.urls import include, path


urlpatterns = [
    path('partners/', include('partners.urls')),
]
