from dal import autocomplete
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from angalabiri.suggestion.models import Suggestion

User = get_user_model()

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Field, Fieldset, Layout, Row, Submit
from crispy_forms.bootstrap import InlineField, UneditableField

from crispy_forms import layout


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ["title", "email", 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="input-group col-md-12"),
                Column("email", css_class="input-group col-md-12"),
                Column("content", css_class="input-group col-md-12"),
                css_class="row mb-0"
            ),
            HTML(
                "<div class='w-100'></div>",
            ),
            Submit(
                "submit",
                "Comment",
                css_class="btn btn-block text-white block rounded-lg py-3 font-weight-semibold text-uppercase mt-3 button-black"
            )
        )
