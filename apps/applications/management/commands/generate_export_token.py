from datetime import UTC, datetime, timedelta

import jwt
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.applications.export import EXPORT_SCOPE


class Command(BaseCommand):
    help = (
        "Генерирует JWT-токен для экспорта анкет активистов: "
        "GET /api/v0/forms/export/?token=<TOKEN>"
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Срок действия токена в днях (по умолчанию 30)",
        )

    def handle(self, *args, **options) -> None:
        now = datetime.now(tz=UTC)
        token = jwt.encode(
            {
                "scope": EXPORT_SCOPE,
                "iat": now,
                "exp": now + timedelta(days=options["days"]),
            },
            settings.FORMS_EXPORT_JWT_SECRET,
            algorithm="HS256",
        )
        self.stdout.write(token)
