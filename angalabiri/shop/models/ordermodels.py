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
    PositiveIntegerField,
    IPAddressField,
    ManyToManyField,
    OneToOneField,
    Q,
    SlugField,
    URLField,
    TextField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# from angalabiri.shop.managers.ordermanagers import OrderManager, ProductPurchaseManager

from angalabiri.shop.models.productmodels import Product
# from angalabiri.shop.models.cartmodels import Cart
# from angalabiri.shop.models.addressmodels import Address
# from angalabiri.shop.models.billingmodels import BillingProfile

# Allorder models
ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


class Order(TimeStampedModel):
    first_name = CharField(max_length=150, null=True)
    last_name = CharField(max_length=150, null=True)
    email = EmailField(null=True)
    address = CharField(max_length=255, null=True)
    postal_code = CharField(max_length=20, null=True)
    city = CharField(max_length=100, null=True)
    paid = BooleanField(default=False, null=True)
    transaction_id = CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created"]

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_absolute_url(self):
        return f"/orders/{self.order_id}"

    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"


class OrderItem(models.Model):
    order = ForeignKey(Order, related_name="items", on_delete=CASCADE)
    product = ForeignKey(Product, related_name="order_items", on_delete=CASCADE)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        return "{}".format(self.id)

    def get_cost(self):
        return self.price * self.quantity
