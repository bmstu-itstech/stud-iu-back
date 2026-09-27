from collections.abc import Callable
from functools import wraps
from http import HTTPStatus

import jwt
from django.conf import settings
from django.http import HttpRequest, HttpResponseBase, JsonResponse

JWT_QUERY_PARAM = "token"
JWT_ALGORITHM = "HS256"


class JwtTokenMiddleware:

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponseBase]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponseBase:
        token = request.GET.get(JWT_QUERY_PARAM)
        if token:
            try:
                request.jwt_claims = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=[JWT_ALGORITHM],
                )
            except jwt.InvalidTokenError:
                request.jwt_claims = None
                request.jwt_error = "invalid"
        return self.get_response(request)


def require_jwt_auth(scope: str | None = None) -> Callable:

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            claims = getattr(self.request, "jwt_claims", None)
            if claims is None:
                detail = (
                    "Invalid or expired token"
                    if getattr(self.request, "jwt_error", None) == "invalid"
                    else "Token is missing"
                )
                return JsonResponse({"detail": detail}, status=HTTPStatus.UNAUTHORIZED)
            if scope is not None and claims.get("scope") != scope:
                return JsonResponse(
                    {"detail": "Token has insufficient scope"},
                    status=HTTPStatus.FORBIDDEN,
                )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
