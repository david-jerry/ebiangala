from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver

from angalabiri.suggestion.models import Suggestion
from angalabiri.utils.models import unique_slug_generator


@receiver(pre_save, sender=Suggestion)
def create_suggestion_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
