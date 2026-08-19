from dmr.routing import Router, path

from .views import ApplicationController, ApplicationDetailController

router = Router(
    prefix="application/",
    urls=[
        path("", ApplicationController.as_view()),
        path("<uuid:application_id>/", ApplicationDetailController.as_view()),
    ],
)
