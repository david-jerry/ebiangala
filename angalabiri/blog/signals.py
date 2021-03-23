from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver

from angalabiri.blog.models import Post
from angalabiri.utils.models import *


@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
