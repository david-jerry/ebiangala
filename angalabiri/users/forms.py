from dal import autocomplete
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from angalabiri.users.models import Addresses

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = [
            "username",
            "status",
            "first_name",
            "mid_name",
            "last_name",
            "gender",
            "photo",
            "dob",
            "lga",
            "email",
            "phone",
            "bvn",
            "accept_terms",
        ]

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserAdminAddressCreateForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = ["user", "flat", "street"]
        widgets = {
            "user": autocomplete.ModelSelect2(url="user-autocomplete"),
        }
