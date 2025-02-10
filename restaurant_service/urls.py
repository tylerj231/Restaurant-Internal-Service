from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app.urls", namespace="app")),
    path("user/", include("user.urls", namespace="user")),
]
