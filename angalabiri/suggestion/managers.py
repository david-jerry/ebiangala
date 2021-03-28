from django.db import models
from django.contrib.contenttypes.models import ContentType

class SuggestionManager(models.Manager):
    def get_queryset(self):
        # All posts
        return super().get_queryset()

    def all_suggestion(self):
        # All posts
        return super().get_queryset().filter(draft=False)

    def all_draft(self):
        # All drafted posts
        return super().get_queryset().filter(draft=True)


