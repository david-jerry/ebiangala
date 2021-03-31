import math
import datetime
from django.conf import settings
from django.db import models
from django.db.models import Count, Sum, Avg
from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver

from angalabiri.shop.models.billingmodels import Card, BillingProfile, Charge
from paystackapi.paystack import Paystack
from django.conf import settings
from django.contrib.auth import get_user_model

from paystackapi.customer import Customer
from paystackapi.verification import Verification

paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)

User = get_user_model()

# import stripe
# STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_cu1lQmcg1OLffhLvYrSCp5XE")
# stripe.api_key = STRIPE_SECRET_KEY



def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST Send to stripe/braintree")
        customer = Customer.create(
                first_name = instance.user.first_name
                last_name=instance.user.last_name,
                email = instance.email
                phone=instance.user.phone,
            )
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)



def new_card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        billing_profile = instance.billing_profile
        qs = Card.objects.filter(billing_profile=billing_profile).exclude(pk=instance.pk)
        qs.update(default=False)


post_save.connect(new_card_post_save_receiver, sender=Card)

