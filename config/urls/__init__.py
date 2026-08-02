from django.contrib import admin
from django.urls import include, path

API_PREFIX = 'api'


urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PREFIX + '/v0/', include('config.urls.v0')),
]

