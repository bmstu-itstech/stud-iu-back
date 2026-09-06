from apps.events.serializers import EventImageSchema


def _images_to_schema(event) -> list[EventImageSchema]:
    return [
        EventImageSchema(id=img.pk, image=img.image.url if img.image else None)
        for img in event.images.all()
    ]
