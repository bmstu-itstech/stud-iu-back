class TokenConfig:
    SECRET_ENV: str = "DJANGO_SECRET_KEY"
    EXPORT_AUDIENCE: str = "export"
    EXPORT_ALGORITHM: str = "HS256"
    MIN_SECRET_LENGTH: int = 32
