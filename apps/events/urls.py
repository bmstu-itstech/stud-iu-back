from dmr.routing import Router, path

from .views import EventDetailController, EventsListController, PastEventsListController

router = Router(
    prefix="events/",
    urls=[
        path("", EventsListController.as_view()),
        path("<uuid:event_id>/", EventDetailController.as_view()),
        path("past/", PastEventsListController.as_view()),
        path("past/<uuid:event_id>/", EventDetailController.as_view()),
    ],
)
