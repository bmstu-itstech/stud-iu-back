from rest_framework import serializers

from partners.models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = (
            'name',
            'url',
            'img',
            'id',
        )
        extra_kwargs = {
            'url': {'required': False},
            'img': {'required': False}
        }