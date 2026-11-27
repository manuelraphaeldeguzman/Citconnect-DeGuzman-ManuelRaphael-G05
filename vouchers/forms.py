from django import forms
from django.utils import timezone

from .models import Voucher, VoucherAssignment


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ["voucher_code"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_voucher_code(self):
        voucher_code = self.cleaned_data["voucher_code"].strip()

        if not voucher_code:
            raise forms.ValidationError("Voucher code cannot be empty.")

        return voucher_code


class VoucherAssignmentForm(forms.ModelForm):
    class Meta:
        model = VoucherAssignment
        fields = ["voucher", "student", "expiration_date"]
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def clean_voucher(self):
        voucher = self.cleaned_data["voucher"]

        existing = VoucherAssignment.objects.filter(voucher=voucher)

        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError(
                "This voucher has already been assigned and cannot be reused."
            )

        return voucher

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data["expiration_date"]

        if expiration_date < timezone.localdate():
            raise forms.ValidationError(
                "Expiration date cannot be in the past."
            )

        return expiration_date