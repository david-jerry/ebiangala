from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        # All posts
        return super().get_queryset().filter(draft=False)

    def featured(self):
        # All posts
        return super().get_queryset().filter(featured=True)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


