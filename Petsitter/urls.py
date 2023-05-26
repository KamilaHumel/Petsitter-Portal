from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("PetsitUser.urls")),
    path("", include("Accounts.urls")),
    path("", include("Services.urls")),
    path("", include("Feedback.urls")),
]
