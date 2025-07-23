from django.urls import include, path
from rest_framework import routers

from events.router import PastEventsViewSet, FutureEventsViewSet

router = routers.DefaultRouter()
router.register(r'past_events', PastEventsViewSet)
router.register(r'future_events', FutureEventsViewSet)

app_name = 'events'
urlpatterns = [
    path('', include(router.urls)),
]
