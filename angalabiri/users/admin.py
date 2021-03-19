from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from angalabiri.users.forms import UserChangeForm, UserCreationForm
from angalabiri.utils.export_as_csv import ExportCsvMixin
from django.utils.safestring import mark_safe

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ExportCsvMixin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_per_page = 250
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": ("first_name", "mid_name", "last_name", "dob", "lga", "email", "phone", "gender", "royals", "status"),
            },
        ),
        (
            _("Security info"),
            {
                "fields": ("bvn",),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "own_shop",
                    "accept_terms",
                    "accept_cookies",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "username",
        "ip_address",
        "accessed_with",
        "dob",
        "lga",
        "photo",
        "is_superuser",
        "last_login",
        "date_joined",
    ]
    search_fields = ["username", "first_name", "mid_name", "last_name", "email", "phone",]
    exclude = [
        "added_by",
    ]

    actions = [
        "export_as_csv",
        "mark_all_users",
        "mark_all_females",
        "mark_all_males",
        "mark_all_chiefs",
    ]

    def mark_all_users(self, request, queryset):
        queryset.update(active=True)

    def mark_all_females(self, request, queryset):
        queryset.update(gender="Female")

    def mark_all_males(self, request, queryset):
        queryset.update(gender="Male")

    def mark_all_chiefs(self, request, queryset):
        queryset.update(royals="Chief")

    def photo(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.photo.url,
                width=obj.photo.width,
                height=obj.photo.height,
            )
        )

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)
