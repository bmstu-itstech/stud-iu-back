from rest_framework import viewsets

from board_members.models import BoardMember
from board_members.serializers import BoardMemberSerializer

from utils.pagination import CustomPagination, CustomListView


class BoardMemberViewSet(CustomListView, viewsets.ModelViewSet):
    queryset = BoardMember.objects.all()
    serializer_class = BoardMemberSerializer
    pagination_class = CustomPagination
