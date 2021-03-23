from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver

from angalabiri.causes.models import Cause
from angalabiri.utils.models import *


@receiver(pre_save, sender=Cause)
def create_cause_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
