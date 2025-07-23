from rest_framework import serializers

from partners.models import Partners


class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = (
            'id',
            'name',
            'url',
            'image',
        )
        extra_kwargs = {
            'url': {'required': False},
            'image': {'required': False},
        }
