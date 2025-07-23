from rest_framework import serializers

from board_members.models import BoardMember


class BoardMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMember
        fields = (
            'id',
            'name',
            'telegram_link',
            'position',
            'start_date',
            'description',
            'image',
        )
        extra_kwargs = {
            'description': {'required': False},
            'image': {'required': False},
        }
