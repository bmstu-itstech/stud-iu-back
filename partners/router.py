from rest_framework import viewsets

from partners.models import Partners
from partners.serializers import PartnersSerializer

from utils.pagination import CustomPagination, CustomListView


class PartnersViewSet(CustomListView, viewsets.ModelViewSet):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer
    pagination_class = CustomPagination
