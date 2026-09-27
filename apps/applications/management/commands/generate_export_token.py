from django.core.management.base import BaseCommand

from apps.applications.jwt_service import create_export_token


class Command(BaseCommand):
    help = (
        "Генерирует JWT-токен для экспорта анкет активистов: "
        "GET /api/v0/application/forms/export/?token=<TOKEN>"
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--days",
            type=int,
            default=None,
            help="Срок действия токена в днях (по умолчанию 30)",
        )

    def handle(self, *args, **options) -> None:
        days = options["days"]
        token = create_export_token(days) if days else create_export_token()
        self.stdout.write(token)
