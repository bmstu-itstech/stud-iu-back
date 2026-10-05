from dmr.routing import Router, path

from .views import EventDetailController, EventListController

router = Router(
    prefix="events/",
    urls=[
        path("", EventListController.as_view()),
        path("<str:event_ref>/", EventDetailController.as_view()),
    ],
)
