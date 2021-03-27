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
    list_display = ["title", "videos", "created", "featured"]
    list_display_links = ["created"]
    list_editable = ["title", "featured"]
    search_fields = ["title", "content"]
    inlines = [PostImagesInline]
    list_per_page = 250
    actions = [
        "export_as_csv",
        "mark_all_posts",
        "mark_all_featured_posts",
        "mark_all_posts_by_me",
    ]


    class Meta:
        model = Post

    def mark_all_posts(self, request, queryset):
        queryset.update(draft=False)

    def mark_all_featured_posts(self, request, queryset):
        queryset.update(draft=False, featured=True)

    def mark_all_posts_by_me(self, request, queryset):
        user = request.user
        queryset.update(author=user)

    # def image(self, obj):
    # def inline_image(self, obj):
    #     return ", ".join([child.image for child in obj.image_set.all()])

    # inline_image.short_description = "image"

    def image(self, obj):
        return mark_safe(
            '<img src="{url}" width="120px" height="auto" />'.format(
                url=obj.image.image.url,
                width=obj.image.image.width,
                height=obj.image.image.height,
            )
        )

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostModelAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'email', 'text']
    list_filter = ['active', 'created']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Image)
