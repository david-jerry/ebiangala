import os
import random

from category.models import Category, Tag
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    TextField,
    ForeignKey,
    GenericIPAddressField,
    PositiveIntegerField,
    ImageField,
    IntegerField,
    IPAddressField,
    ManyToManyField,
    OneToOneField,
    Q,
    SlugField,
    URLField,
)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from .managers import SuggestionManager

# Create your models here.
class Suggestion(TimeStampedModel):
    title = CharField(_("Post Title"), blank=False, null=True, max_length=255)
    slug = SlugField(unique=True, null=True, blank=True, max_length=500)
    url = URLField(blank=True, max_length=500, null=True, unique=True)
    pub_date = DateField(
        _("Suggestion Published Date"),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=False,
    )
    draft = BooleanField(default=False)
    featured = BooleanField(default=False)
    content = TextField()
    objects = SuggestionManager()

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = "Suggestion"
        verbose_name_plural = "Suggestions"
        ordering = ["title", "-pub_date"]

    def get_absolute_url(self):
        return f"/suggestion/{self.slug}"

    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"
