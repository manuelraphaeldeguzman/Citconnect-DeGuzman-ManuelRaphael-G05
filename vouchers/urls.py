from django.urls import path
from . import views

urlpatterns = [
    path("", views.VoucherListView.as_view(), name="voucher-list"),
    path("create/", views.VoucherCreateView.as_view(), name="voucher-create"),
    path("<int:pk>/edit/", views.VoucherUpdateView.as_view(), name="voucher-update"),
    path("<int:pk>/delete/", views.VoucherDeleteView.as_view(), name="voucher-delete"),
    path("assignments/", views.VoucherAssignmentListView.as_view(), name="assignment-list"),
    path("assignments/create/", views.VoucherAssignmentCreateView.as_view(), name="assignment-create"),
    path("assignments/<int:pk>/edit/", views.VoucherAssignmentUpdateView.as_view(), name="assignment-update"),
    path("assignments/<int:pk>/delete/", views.VoucherAssignmentDeleteView.as_view(), name="assignment-delete"),

]