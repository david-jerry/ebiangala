from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from angalabiri.suggestion.models import Suggestion
from angalabiri.utils.export_as_csv import ExportCsvMixin

# Register your models here.
class SuggestionModelAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["title", "created", "draft", "featured"]
    list_display_links = ["title"]
    list_editable = ["draft", "featured"]
    search_fields = ["title", "content"]
    list_per_page = 250
    actions = [
        "export_as_csv",
        "mark_all_suggestions",
        "mark_all_featured_suggestions",
    ]


    class Meta:
        model = Suggestion

    def mark_all_suggestions(self, request, queryset):
        queryset.update(draft=False)

    def mark_all_featured_suggestions(self, request, queryset):
        queryset.update(draft=False, featured=True)

admin.site.register(Suggestion, SuggestionModelAdmin)
