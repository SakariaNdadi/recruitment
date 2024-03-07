from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="RMS API",
        default_version="v1",
        description="A Web API for managing Telecom Namibia Limited Recruitment System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ndadis@telecom.na"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)


urlpatterns = [
    # APIs
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("apps.api.urls")),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "api/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("__debug__/", include("debug_toolbar.urls")),
    # Documentation and Schema
    path("", include("apps.pages.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("recruitment/", include("apps.recruitment.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
]
if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif settings.DEBUG == False:
    urlpatterns += [path("telecomsuperuseradministration/", admin.site.urls)]
