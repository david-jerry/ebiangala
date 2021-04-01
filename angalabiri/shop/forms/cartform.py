from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 20)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, required=False)
    update = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)