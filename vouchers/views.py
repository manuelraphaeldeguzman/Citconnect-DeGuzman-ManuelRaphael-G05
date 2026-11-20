from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Voucher
from .forms import VoucherForm


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.role == "STAFF"
            and hasattr(self.request.user, "staff_profile")
        )


class VoucherListView(StaffRequiredMixin, ListView):
    model = Voucher
    template_name = "vouchers/voucher_list.html"
    context_object_name = "vouchers"
    ordering = ["-created_at"]


class VoucherCreateView(StaffRequiredMixin, CreateView):
    model = Voucher
    form_class = VoucherForm
    template_name = "vouchers/voucher_form.html"
    success_url = reverse_lazy("voucher-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.staff_profile
        messages.success(self.request, "Voucher created successfully!")
        return super().form_valid(form)


class VoucherUpdateView(StaffRequiredMixin, UpdateView):
    model = Voucher
    form_class = VoucherForm
    template_name = "vouchers/voucher_form.html"
    success_url = reverse_lazy("voucher-list")

    def form_valid(self, form):
        messages.success(self.request, "Voucher updated successfully!")
        return super().form_valid(form)


class VoucherDeleteView(StaffRequiredMixin, DeleteView):
    model = Voucher
    template_name = "vouchers/voucher_confirm_delete.html"
    success_url = reverse_lazy("voucher-list")

    def form_valid(self, form):
        messages.success(self.request, "Voucher deleted successfully!")
        return super().form_valid(form)