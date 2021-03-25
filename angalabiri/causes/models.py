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
    ForeignKey,
    GenericIPAddressField,
    ImageField,
    IntegerField,
    IPAddressField,
    ManyToManyField,
    OneToOneField,
    Q,
    SlugField,
    URLField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from .managers import CauseManager

# Create your models here.


User = settings.AUTH_USER_MODEL


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# def cause_file_path(filename, instance):
#     new_filename = random.randint(1, 3910209312)
#     name, ext = get_filename_ext(filename)
#     final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
#     return "causes/{new_filename}/{final_filename}".format(
#         new_filename=new_filename, final_filename=final_filename
#     )
def cause_file_path(instance, filename):
    return "causes/{filename}".format(filename=filename)

class Cause(TimeStampedModel):
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    title = CharField(_("Cause Title"), blank=False, null=True, max_length=255)
    slug = SlugField(unique=True, null=True, blank=True, max_length=500)
    image = ImageField(
        _("Upload Image"),
        upload_to=cause_file_path,
        null=True,
        blank=True,
    )
    pub_date = DateField(
        _("Post Published Date"),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=False,
    )
    end_date = DateField(
        _("End Published Date"),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=False,
    )
    tt_amount = DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    donate = DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=0.00)
    max_donation = DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, default=100000.00)
    draft = BooleanField(default=False)
    featured = BooleanField(default=False)
    content = RichTextUploadingField()
    added_by = CharField(_("added_by"), max_length=255, null=True, blank=True)
    categories = ManyToManyField("category.Category", help_text="Categorize this item.")
    tags = ManyToManyField("category.Tag", help_text="Tag this item.")
    objects = CauseManager()

    def __str__(self):
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return "title", "author.title"

    @property
    def avg(self):
        dec = self.tt_amount / self.max_donation
        avg = dec * 100
        return avg


    def save(self, *args, **kwargs):
        if self.max_donation > self.tt_amount:
            self.tt_amount = self.tt_amount + self.donate
        else:
            self.draft = True
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        verbose_name = "Cause"
        verbose_name_plural = "Causes"
        ordering = ["title", "-end_date"]

    def get_absolute_url(self):
        return f"/cause/{self.slug}"

    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"
