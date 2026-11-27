from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("dashboard.urls")),
    path("vouchers/", include("vouchers.urls")),
]
handler404 = "citconnect.views.custom_404"
handler500 = "citconnect.views.custom_500"