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

from angalabiri.shop.models.ordermodels import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     BaseInput("quantity", value=1, style="width:50px;", add_class="qty"),
        #     Submit("Add To Cart", "Add To Cart", css_class="add-to-cart button m-0"),
        # )
