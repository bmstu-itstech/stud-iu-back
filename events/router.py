from rest_framework import viewsets

from events.models import PastEvents, FutureEvents
from events.serializers import PastEventsSerializer, FutureEventsSerializer
from utils.pagination import CustomPagination, CustomListView


class PastEventsViewSet(CustomListView, viewsets.ModelViewSet):
    queryset = PastEvents.objects.all()
    serializer_class = PastEventsSerializer
    pagination_class = CustomPagination


class FutureEventsViewSet(CustomListView, viewsets.ModelViewSet):
    queryset = FutureEvents.objects.all()
    serializer_class = FutureEventsSerializer
    pagination_class = CustomPagination
