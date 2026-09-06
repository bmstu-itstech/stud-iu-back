from dmr.routing import Router, path

from .views import (
    FutureEventDetailController,
    FutureEventListController,
    PastEventDetailController,
    PastEventListController,
)

router = Router(
    prefix="events/",
    urls=[
        path("", FutureEventListController.as_view()),
        path("<uuid:event_id>/", FutureEventDetailController.as_view()),
        path("past/", PastEventListController.as_view()),
        path("past/<uuid:event_id>/", PastEventDetailController.as_view()),
    ],
)
