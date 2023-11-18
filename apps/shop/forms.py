from django import forms
from django.core.exceptions import ValidationError

from .models import CartProduct


class CartProductForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ("size", "color", "quantity")

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity <= 0:
            raise ValidationError("Min quantity is 1")

        return quantity  