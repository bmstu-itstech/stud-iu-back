from django.urls import include
from dmr.routing import Router, path

from apps.board_members import urls as board_members_urls
from apps.events import urls as events_urls
from apps.news import urls as news_urls
from apps.partners import urls as partners_urls

router = Router(
    prefix="api/v0/",
    urls=[
        path(
            board_members_urls.router.prefix,
            include(
                (board_members_urls.router.urls, "board_members"),
                namespace="board_members",
            ),
        ),
        path(
            events_urls.router.prefix,
            include(
                (events_urls.router.urls, "events"),
                namespace="events",
            ),
        ),
        path(
            news_urls.router.prefix,
            include(
                (news_urls.router.urls, "news"),
                namespace="news",
            ),
        ),
        path(
            partners_urls.router.prefix,
            include(
                (partners_urls.router.urls, "partners"),
                namespace="partners",
            ),
        ),
    ],
)

urlpatterns = router.urls
