
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

from angalabiri.shop.models.billingmodels import BillingProfile

from model_utils.models import StatusModel, TimeStampedModel


ADDRESS_TYPES = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)

class Address(TimeStampedModel):
    billing_profile = ForeignKey(BillingProfile, on_delete=SET_NULL, null=True)
    name            = CharField(max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
    nickname        = CharField(max_length=120, null=True, blank=True, help_text='Internal Reference Nickname')
    address_type    = CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1  = CharField(max_length=120)
    address_line_2  = CharField(max_length=120, null=True, blank=True)
    city            = CharField(max_length=120)
    country         = CharField(max_length=120, default='United States of America')
    state           = CharField(max_length=120)
    postal_code     = CharField(max_length=120)

    def __str__(self):
        if self.nickname:
            return str(self.nickname)
        return str(self.address_line_1)

    def get_absolute_url(self):
        return reverse("address-update", kwargs={"pk": self.pk})

    def get_short_address(self):
        for_name = self.name 
        if self.nickname:
            for_name = "{} | {},".format( self.nickname, for_name)
        return "{for_name} {line1}, {city}".format(
                for_name = for_name or "",
                line1 = self.address_line_1,
                city = self.city
            ) 

    def get_address(self):
        return "{for_name}\n{line1}\n{line2}\n{city}\n{state}, {postal}\n{country}".format(
                for_name = self.name or "",
                line1 = self.address_line_1,
                line2 = self.address_line_2 or "",
                city = self.city,
                state = self.state,
                postal= self.postal_code,
                country = self.country
            )