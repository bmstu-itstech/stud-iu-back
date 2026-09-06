from dmr.routing import Router, path

from .views import (
    ApplicationController,
    ApplicationDetailController,
    ApplicationFormSchemaController,
)

router = Router(
    prefix="application/",
    urls=[
        path("schema/", ApplicationFormSchemaController.as_view()),
        path("", ApplicationController.as_view()),
        path("<uuid:application_id>/", ApplicationDetailController.as_view()),
    ],
)
