from dmr.routing import Router, path

from .views import BoardMemberDetailController, BoardMemberListController

router = Router(
    prefix="board-members/",
    urls=[
        path("", BoardMemberListController.as_view()),
        path("<uuid:board_member_id>/", BoardMemberDetailController.as_view()),
    ],
)
