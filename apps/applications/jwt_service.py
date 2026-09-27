from datetime import UTC, datetime, timedelta

import jwt
from django.conf import settings

EXPORT_SCOPE = "forms_export"
JWT_ALGORITHM = "HS256"
DEFAULT_TOKEN_LIFETIME_DAYS = 30


def create_export_token(days: int = DEFAULT_TOKEN_LIFETIME_DAYS) -> str:
    now = datetime.now(tz=UTC)
    return jwt.encode(
        {
            "scope": EXPORT_SCOPE,
            "iat": now,
            "exp": now + timedelta(days=days),
        },
        settings.SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        return None
