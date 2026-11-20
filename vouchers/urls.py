from django.urls import path
from . import views

urlpatterns = [
    path("", views.VoucherListView.as_view(), name="voucher-list"),
    path("create/", views.VoucherCreateView.as_view(), name="voucher-create"),
    path("<int:pk>/edit/", views.VoucherUpdateView.as_view(), name="voucher-update"),
    path("<int:pk>/delete/", views.VoucherDeleteView.as_view(), name="voucher-delete"),
]