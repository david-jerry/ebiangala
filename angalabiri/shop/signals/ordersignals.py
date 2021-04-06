# import math
# import datetime
# from django.conf import settings
# from django.db import models
# from django.db.models import Count, Sum, Avg
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import Signal, receiver

# from angalabiri.shop.models.productmodels import Product, ProductFile, ProductVariation, ProductionImage
# from .models.cartmodels import Cart
# from .models.ordermodels import Order
# from .models.addressmodels import Address
# from angalabiri.utils.models import *

# def pre_save_create_order_id(sender, instance, *args, **kwargs):
#     if not instance.order_id:
#         instance.order_id = unique_order_id_generator(instance)
#     qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
#     if qs.exists():
#         qs.update(active=False)

#     if instance.shipping_address and not instance.shipping_address_final:
#         instance.shipping_address_final = instance.shipping_address.get_address()

#     if instance.billing_address and not instance.billing_address_final:
#         instance.billing_address_final = instance.billing_address.get_address()


# pre_save.connect(pre_save_create_order_id, sender=Order)


# def post_save_cart_total(sender, instance, created, *args, **kwargs):
#     if not created:
#         cart_obj = instance
#         cart_total = cart_obj.total
#         cart_id = cart_obj.id
#         qs = Order.objects.filter(cart__id=cart_id)
#         if qs.count() == 1:
#             order_obj = qs.first()
#             order_obj.update_total()

# post_save.connect(post_save_cart_total, sender=Cart)


# def post_save_order(sender, instance, created, *args, **kwargs):
#     #print("running")
#     if created:
#         print("Updating... first")
#         instance.update_total()


# post_save.connect(post_save_order, sender=Order)


import math
import datetime
from django.conf import settings
from django.db import models
from django.db.models import Count, Sum, Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver


from angalabiri.shop.models.ordermodels import Order
from angalabiri.shop.models.addressmodels import Address
from angalabiri.utils.models import unique_slug_generator

from paystackapi.transactions import Transaction

@receiver(pre_save, sender=Order)
def create_initialized_order_id(sender, instance, *args, **kwargs):
    if not instance.transaction_id:
        transaction = Transaction.initialize(
            reference=f"ANGALASHOP_ORDERNO_{instance.id}",
            amount='{:.2f}'.format(instance.get_total_cost()) * 100,
            email=instance.email,
            **kwargs
        )
        instance.transaction_id = transaction.id


