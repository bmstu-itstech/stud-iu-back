from dmr.routing import Router, path

from .views import PartnerDetailController, PartnerListController

router = Router(
    prefix="partners/",
    urls=[
        path("", PartnerListController.as_view()),
        path("<uuid:partner_id>/", PartnerDetailController.as_view()),
    ],
)
