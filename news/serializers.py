from rest_framework import serializers

from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'description',
            'cover_url',
            'created_at',
        )

        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'title': {'required': True, 'max_length': 128},
            'cover_url': {'required': True},
            'created_at': {'required': True},
        }
        
        read_only_fields = ('id', )
