import random
import os
import math
import datetime
from decimal import Decimal
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
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

from angalabiri.shop.managers.cartmanagers import CartManager
from angalabiri.shop.models.productmodels import Product, ProductVariation


User = settings.AUTH_USER_MODEL

# Start Cart models
class Cart(TimeStampedModel):
    user        = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    products    = ManyToManyField(Product, blank=True)
    subtotal    = DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = DecimalField(default=0.00, max_digits=100, decimal_places=2)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def is_digital(self):
        qs = self.products.all() #every product
        new_qs = qs.filter(is_digital=False) # every product that is not digial
        if new_qs.exists():
            return False
        return True

# End cart models
