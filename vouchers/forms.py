from django import forms
from .models import Voucher


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ["voucher_code"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })