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
    list_display = ["title", "image", "created", "featured"]
    list_display_links = ["created"]
    list_editable = ["title", "featured"]
    search_fields = ["title", "content"]
    list_per_page = 250

    class Meta:
        model = Cause

        actions = [
            "export_as_csv",
            "mark_all_cause",
            "mark_all_featured_cause",
            "mark_all_cause_by_me",
        ]

    def mark_all_cause(self, request, queryset):
        queryset.update(draft=False)

    def mark_all_featured_cause(self, request, queryset):
        queryset.update(featured=True)

    def mark_all_cause_by_me(self, request, queryset):
        user = request.user
        queryset.update(author=user)

    def image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.images.image.url,
                width=obj.images.image.width,
                height=obj.images.image.height,
            )
        )

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Cause, CauseModelAdmin)
