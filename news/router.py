from rest_framework import viewsets

from news.models import News
from news.serializers import NewsSerializer
from utils.pagination import CustomPagination, CustomListView


class NewsViewSet(CustomListView, viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = CustomPagination
