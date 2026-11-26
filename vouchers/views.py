from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Voucher, VoucherAssignment
from .forms import VoucherForm, VoucherAssignmentForm


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


# VOUCHER ASSIGNMENT CRUD

class VoucherAssignmentListView(StaffRequiredMixin, ListView):
    model = VoucherAssignment
    template_name = "vouchers/assignment_list.html"
    context_object_name = "assignments"

    def get_queryset(self):
        return VoucherAssignment.objects.select_related(
            "voucher",
            "student__user",
            "assigned_by__user"
        ).order_by("-assigned_at")


class VoucherAssignmentCreateView(StaffRequiredMixin, CreateView):
    model = VoucherAssignment
    form_class = VoucherAssignmentForm
    template_name = "vouchers/assignment_form.html"
    success_url = reverse_lazy("assignment-list")

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user.staff_profile
        messages.success(self.request, "Voucher assigned successfully!")
        return super().form_valid(form)


class VoucherAssignmentUpdateView(StaffRequiredMixin, UpdateView):
    model = VoucherAssignment
    form_class = VoucherAssignmentForm
    template_name = "vouchers/assignment_form.html"
    success_url = reverse_lazy("assignment-list")

    def form_valid(self, form):
        messages.success(self.request, "Voucher assignment updated successfully!")
        return super().form_valid(form)


class VoucherAssignmentDeleteView(StaffRequiredMixin, DeleteView):
    model = VoucherAssignment
    template_name = "vouchers/assignment_confirm_delete.html"
    success_url = reverse_lazy("assignment-list")

    def form_valid(self, form):
        messages.success(self.request, "Voucher assignment deleted successfully!")
        return super().form_valid(form)