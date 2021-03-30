import math
import datetime
from django.conf import settings
from django.db import models
from django.db.models import Count, Sum, Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver

from angalabiri.shop.models.productmodels import Product, ProductFile, ProductVariation, ProductionImage
from angalabiri.shop.models.cartmodels import Cart


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)




def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.08) # 8% tax
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)




