from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Column,
    HTML,
    Field,
    Fieldset,
    Layout,
    Row,
    Submit,
    BaseInput,
)
from crispy_forms.bootstrap import InlineField, UneditableField
from crispy_forms import layout

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 200)]


class CartAddProductForm(forms.Form):

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        required=False,
        widget=forms.TextInput(attrs={'class': 'qty', 'style':'width:60px; padding: 8.7px;'})
    )
    update = forms.BooleanField(
        widget=forms.HiddenInput(), initial=False, required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BaseInput("quantity", value=1, style="width:50px;", add_class="qty"),
            Submit("Add To Cart", "Add To Cart", css_class="add-to-cart button m-0"),
        )
