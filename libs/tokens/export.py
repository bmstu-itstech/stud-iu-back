import datetime as dt
import uuid

from dmr.security.jwt.token import JWToken

from libs.tokens.config import TokenConfig
from libs.tokens.exceptions import TokenSecretError


def validate_secret(secret: str | None) -> str:
    if not secret:
        raise TokenSecretError(
            f"Переменная окружения {TokenConfig.SECRET_ENV} не задана"
        )
    if len(secret) < TokenConfig.MIN_SECRET_LENGTH:
        raise TokenSecretError(
            "Длина секрета для формирования jwt-токена должна быть не менее "
            f"{TokenConfig.MIN_SECRET_LENGTH}, получено {len(secret)}",
        )
    return secret


def issue_export_token(secret: str, lifetime: dt.timedelta) -> str:
    return JWToken(
        sub=TokenConfig.EXPORT_AUDIENCE,
        aud=TokenConfig.EXPORT_AUDIENCE,
        exp=dt.datetime.now(dt.UTC) + lifetime,
        jti=uuid.uuid4().hex,
    ).encode(
        secret=validate_secret(secret),
        algorithm=TokenConfig.EXPORT_ALGORITHM,
    )
