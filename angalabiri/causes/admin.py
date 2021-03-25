from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from angalabiri.causes.models import Cause
from angalabiri.utils.export_as_csv import ExportCsvMixin
from angalabiri.causes.forms import CauseCreateForm

# Register your models here.
class CauseModelAdmin(admin.ModelAdmin, ExportCsvMixin):
    add_form = CauseCreateForm()
    list_display = ["title", "photo", "created", "featured"]
    list_display_links = ["created"]
    list_editable = ["title", "featured"]
    search_fields = ["title", "content"]
    list_per_page = 250
    actions = [
        "export_as_csv",
        "mark_all_cause_draft",
        "mark_all_cause_featured",
        "unmark_all_cause_featured",
        "mark_all_cause_by_me",
    ]


    class Meta:
        model = Cause

    def mark_all_cause_draft(self, request, queryset):
        for obj in queryset:
            obj.draft = True
        queryset.update(draft=True)

    def mark_all_cause_featured(self, request, queryset):
        for obj in queryset:
            obj.featured = True
        queryset.update(featured=True)

    def unmark_all_cause_featured(self, request, queryset):
        for obj in queryset:
            obj.featured = False
        queryset.update(featured=False)

    def mark_all_cause_by_me(self, request, queryset):
        user = request.user
        queryset.update(author=user)

    def photo(self, obj):
        return mark_safe(
            '<img src="{url}" width="150px" height="auto" />'.format(
                url=obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
            )
        )

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user.username
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Cause, CauseModelAdmin)
