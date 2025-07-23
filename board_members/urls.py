from django.urls import include, path
from rest_framework import routers

from board_members.router import BoardMemberViewSet

router = routers.DefaultRouter()
router.register('', BoardMemberViewSet)

app_name = 'board_members'
urlpatterns = [
    path('', include(router.urls)),
]
