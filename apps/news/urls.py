from dmr.routing import Router, path

from .views import NewsDetailController, NewsListController

router = Router(
    prefix="news/",
    urls=[
        path("", NewsListController.as_view()),
        path("<uuid:news_id>/", NewsDetailController.as_view()),
    ],
)
