from dmr.routing import Router, path

from .views import EventDetailController, EventListController

router = Router(
    prefix="events/",
    urls=[
        path("", EventListController.as_view()),
        path("<uuid:event_id>/", EventDetailController.as_view()),
    ],
)
