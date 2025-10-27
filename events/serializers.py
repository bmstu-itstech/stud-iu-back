from rest_framework import serializers

from events.models import (
    Events,
    PastEvents,
    FutureEvents,
    EventImages
)


class EventImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImages
        fields = "__all__"


class EventsSerializer(serializers.ModelSerializer):
    date_range = serializers.SerializerMethodField()

    images = EventImagesSerializer(
        many=True,
        read_only=True,
        source='events_images'
    )
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
        default=list,
    )

    class Meta:
        model = Events
        fields = (
            'id',
            'name',
            'description',
            'color',
            'start_datetime',
            'end_datetime',
            'date_range',
            'images',
            'uploaded_images',
        )

        extra_kwargs = {
            'start_datetime': {'required': True},
            'end_datetime': {'required': False},
        }

        read_only_fields = ('id', 'date_range', )

    def get_date_range(self, object):
        return object.date_range_display

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])

        if self.Meta.model == PastEvents:
            album_link = validated_data.pop('album_link', None)
            event = self.Meta.model.objects.create(
                album_link=album_link, **validated_data
            )
        else:
            registration_link = validated_data.pop('registration_link', None)
            event = self.Meta.model.objects.create(
                registration_link=registration_link, **validated_data
            )

        for image in uploaded_images:
            if isinstance(event, PastEvents):
                EventImages.objects.create(past_event=event, image=image)
            else:
                EventImages.objects.create(future_event=event, image=image)

        return event


class PastEventsSerializer(EventsSerializer):
    class Meta(EventsSerializer.Meta):
        model = PastEvents
        fields = '__all__'


class FutureEventsSerializer(EventsSerializer):
    class Meta(EventsSerializer.Meta):
        model = FutureEvents
        fields = '__all__'
