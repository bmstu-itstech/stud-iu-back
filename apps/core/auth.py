from typing import Self, override

from django.http import HttpRequest
from dmr.controller import Controller
from dmr.endpoint import Endpoint
from dmr.openapi.objects import Reference, SecurityScheme
from dmr.security.jwt import JWTSyncAuth
from dmr.serializer import BaseSerializer

from libs.tokens import TokenConfig


class QueryJWTSyncAuth(JWTSyncAuth):
    __slots__ = ("query_param",)

    def __init__(self, *, query_param: str = "token") -> None:
        super().__init__(
            algorithm=TokenConfig.EXPORT_ALGORITHM,
            accepted_audiences=TokenConfig.EXPORT_AUDIENCE,
            require_claims=("exp", "jti"),
        )
        self.query_param = query_param

    @property
    @override
    def security_schemes(self) -> dict[str, SecurityScheme | Reference]:
        return {
            self.security_scheme_name: SecurityScheme(
                type="apiKey",
                name=self.query_param,
                security_scheme_in="query",
                description="JWT token auth via query string",
            ),
        }

    @override
    def get_token_from_request(self, request: HttpRequest) -> str | None:
        return request.GET.get(self.query_param)

    @override
    def split_encoded_token(self, header: str) -> str | None:
        return header

    @override
    def __call__(
        self,
        endpoint: Endpoint,
        controller: Controller[BaseSerializer],
    ) -> Self | None:
        if self.prepare_token(controller.request) is None:
            return None
        return self
