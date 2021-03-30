from django.conf import settings
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
from angalabiri.shop.managers.billingmanagers import *


User = settings.AUTH_USER_MODEL




class BillingProfile(TimeStampedModel):
    user        = OneToOneField(User, null=True, blank=True)
    email       = EmailField()
    active      = BooleanField(default=True)
    customer_id = CharField(max_length=120, null=True, blank=True)
    # customer_id in Stripe or Braintree

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    def get_payment_method_url(self):
        return reverse('billing-payment-method')

    @property
    def has_card(self): # instance.has_card
        card_qs = self.get_cards()
        return card_qs.exists() # True or False

    @property
    def default_card(self):
        default_cards = self.get_cards().filter(active=True, default=True)
        if default_cards.exists():
            return default_cards.first()
        return None

    def set_cards_inactive(self):
        cards_qs = self.get_cards()
        cards_qs.update(active=False)
        return cards_qs.filter(active=True).count()





class Card(models.Model):
    billing_profile         = ForeignKey(BillingProfile)
    stripe_id               = CharField(max_length=120)
    brand                   = CharField(max_length=120, null=True, blank=True)
    country                 = CharField(max_length=20, null=True, blank=True)
    exp_month               = IntegerField(null=True, blank=True)
    exp_year                = IntegerField(null=True, blank=True)
    last4                   = CharField(max_length=4, null=True, blank=True)
    default                 = BooleanField(default=True)
    active                  = BooleanField(default=True)
    timestamp               = DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)




class Charge(models.Model):
    billing_profile         = ForeignKey(BillingProfile)
    stripe_id               = CharField(max_length=120)
    paid                    = BooleanField(default=False)
    refunded                = BooleanField(default=False)
    outcome                 = TextField(null=True, blank=True)
    outcome_type            = CharField(max_length=120, null=True, blank=True)
    seller_message          = CharField(max_length=120, null=True, blank=True)
    risk_level              = CharField(max_length=120, null=True, blank=True)

    objects = ChargeManager()

