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
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from angalabiri.shop.managers.ordermanagers import *

from angalabiri.shop.models.productmodels import Product
from angalabiri.shop.models.cartmodels import Cart
from angalabiri.shop.models.ordermodels import Order
from angalabiri.shop.models.addressmodels import Address
from angalabiri.shop.models.billingmodels import BillingProfile

# Allorder models
class ProductPurchase(TimeStampedModel):
    order_id            = CharField(max_length=120)
    billing_profile     = ForeignKey(BillingProfile, null=True, on_delete=SET_NULL, related_name="billing_info") # billingprofile.productpurchase_set.all()
    product             = ForeignKey(Product, null=True, on_delete=SET_NULL, related_name="product_purchase") # product.productpurchase_set.count()
    refunded            = BooleanField(default=False)

    objects = ProductPurchaseManager()

    def __str__(self):
        return self.product.title

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class Order(TimeStampedModel):
    billing_profile     = ForeignKey(BillingProfile, on_delete=SET_NULL, null=True, blank=True)
    order_id            = CharField(max_length=255, blank=True) # AB31DE3
    shipping_address    = ForeignKey(Address, related_name="shipping_address",null=True, on_delete=SET_NULL, blank=True)
    billing_address     = ForeignKey(Address, related_name="billing_address", null=True, on_delete=SET_NULL, blank=True)
    shipping_address_final    = TextField(blank=True, null=True)
    billing_address_final     = TextField(blank=True, null=True)
    cart                = ForeignKey(Cart, on_delete=SET_NULL, null=True)
    status              = CharField(max_length=255, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total      = DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total               = DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active              = BooleanField(default=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    class Meta:
       ordering = ['-created', '-updated']

    def get_absolute_url(self):
        return f"/orders/{self.order_id}"

    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"


    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping Soon"

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        shipping_address_required = not self.cart.is_digital
        shipping_done = False
        if shipping_address_required and self.shipping_address:
            shipping_done = True
        elif shipping_address_required and not self.shipping_address:
            shipping_done = False
        else:
            shipping_done = True
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total   = self.total
        if billing_profile and shipping_done and billing_address and total > 0:
            return True
        return False

    def update_purchases(self):
        for p in self.cart.products.all():
            obj, created = ProductPurchase.objects.get_or_create(
                    order_id=self.order_id,
                    product=p,
                    billing_profile=self.billing_profile
                )
        return ProductPurchase.objects.filter(order_id=self.order_id).count()

    def mark_paid(self):
        if self.status != 'paid':
            if self.check_done():
                self.status = "paid"
                self.save()
                self.update_purchases()
        return self.status


# end all order models



class ProductPurchase(TimeStampedModel):
    order_id            = models.CharField(max_length=120)
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=SET_NULL, null=True) # billingprofile.productpurchase_set.all()
    product             = models.ForeignKey(Product, on_delete=SET_NULL, null=True) # product.productpurchase_set.count()
    refunded            = models.BooleanField(default=False)

    objects = ProductPurchaseManager()

    def __str__(self):
        return self.product.title

