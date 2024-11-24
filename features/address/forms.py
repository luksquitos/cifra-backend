from django import forms
from features.address import models
from widgets.input_mask import InputMask


class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = [
            "postal_code",
            "street",
            "district",
            "city",
            "state",
            "number",
            "complement",
        ]
        widgets = {"postal_code": InputMask("99999-999")}
