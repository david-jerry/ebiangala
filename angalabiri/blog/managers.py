from django.db import models


class PostManager(models.Manager):
    def get_queryset(self):
        # All posts
        return super().get_queryset()

    def all_posts(self):
        # All posts
        return super().get_queryset().filter(draft=False)

    def all_draft(self):
        # All drafted posts
        return super().get_queryset().filter(draft=True)
