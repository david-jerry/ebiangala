import math
import datetime
from django.conf import settings
from django.db import models
from django.db.models import Count, Sum, Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver

from angalabiri.shop.models.productmodels import Product, ProductFile, ProductVariation, ProductionImage
from .models.cartmodels import Cart
from .models.ordermodels import Order
from .models.addressmodels import Address
from angalabiri.utils.models import *


@receiver(pre_save, sender=Product)
def create_product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)




def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
	product = instance
	variations = product.variation_set.all()
	if variations.count() == 0:
		new_var = Variation()
		new_var.product = product
		new_var.title = "Default"
		new_var.price = product.price + new_var.price
		new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)





