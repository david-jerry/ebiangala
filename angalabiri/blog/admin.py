from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from angalabiri.blog.models import Category, Comment, Image, Post
from angalabiri.utils.export_as_csv import ExportCsvMixin


# Register your models here.
class PostImagesInline(admin.StackedInline):
    model = Image


class PostModelAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["title", "videos", "inline_image", "created", "featured"]
    list_display_links = ["created"]
    list_editable = ["title", "featured"]
    search_fields = ["title", "content"]
    inlines = [PostImagesInline]
    list_per_page = 250

    class Meta:
        model = Post

        actions = [
            "export_as_csv",
            "mark_all_posts",
            "mark_all_featured_posts",
            "mark_all_posts_by_me",
        ]

    def mark_all_posts(self, request, queryset):
        queryset.update(draft=False)

    def mark_all_featured_posts(self, request, queryset):
        queryset.update(draft=False, featured=True)

    def mark_all_posts_by_me(self, request, queryset):
        user = request.user
        queryset.update(author=user)

    # def image(self, obj):
    def inline_image(self, obj):
        return ", ".join([child.images for child in obj.images.all()])

    inline_image.short_description = "image"

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


admin.site.register(Post, PostModelAdmin)

admin.site.register(Comment)
admin.site.register(Image)
