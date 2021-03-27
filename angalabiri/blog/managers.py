from django.db import models
from django.contrib.contenttypes.models import ContentType

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


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return super().get_queryset().filter(parent=None)


    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        return super().get_queryset().filter(content_type=content_type, object_id= obj_id).filter(parent=None)
