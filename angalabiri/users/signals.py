from django.http import request
from django.contrib.auth import get_user_model


from paystackapi.paystack import Paystack
from config import settings

from paystackapi.customer import Customer
from paystackapi.verification import Verification

from django.db.models.signals import post_save, pre_save
from  django.dispatch import receiver

paystack_secret_key = settings.base.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)

User = get_user_model()


@receiver(pre_save, sender=User)
def create_paystack_customer(sender, instance, *args, **kwargs):
    customer = Customer.create(
        first_name=instance.first_name,
        last_name=instance.last_name,
        email=instance.email,
        phone=instance.phone,
    )

@receiver(post_save, sender=User)
def create_paystack_customer(sender, instance, created, *args, **kwargs):
    if created:
        customer = Customer.update(
        first_name=instance.first_name,
        last_name=instance.last_name,
        email=instance.email,
        phone=instance.phone,
    )
