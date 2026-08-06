from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from dmr.openapi import build_schema
from dmr.openapi.views import OpenAPIJsonView, SwaggerView

from config.urls.v0 import router as v0_router

API_PREFIX = "api"


urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PREFIX + "/v0/", include("config.urls.v0")),
]

if settings.DEBUG:
    schema = build_schema(v0_router)

    urlpatterns += [
        path("docs/openapi.json/", OpenAPIJsonView.as_view(schema), name="openapi"),
        path("docs/swagger/", SwaggerView.as_view(schema), name="swagger"),
    ]
