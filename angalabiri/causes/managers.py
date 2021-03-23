from django.db import models


class CauseManager(models.Manager):
    def get_queryset(self):
        # All posts
        return super().get_queryset().filter(draft=False)

    def featured(self):
        # All posts
        return super().get_queryset().filter(featured=True)
