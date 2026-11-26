
from django import forms
from .models import Voucher, VoucherAssignment


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ["voucher_code"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


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
