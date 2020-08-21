"""traktor URL Configuration."""

from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v0/", include("traktor.views.api.v0.urls")),
] + staticfiles_urlpatterns()
