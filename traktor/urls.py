"""traktor URL Configuration."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/", include("traktor.views.api.v0.urls")),
]
