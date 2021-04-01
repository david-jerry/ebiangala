from django.db import models
from paystackapi.paystack import Paystack
from django.conf import settings
from django.contrib.auth import get_user_model

from paystackapi.customer import Customer
from paystackapi.verification import Verification

paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack = Paystack(secret_key=paystack_secret_key)

User = get_user_model()

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        # guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated():
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                            user=user, email=user.email)
        # elif guest_email_id is not None:
        #     'guest user checkout; auto reloads payment stuff'
        #     guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        #     obj, created = self.model.objects.get_or_create(
        #                                     email=guest_email_obj.email)
        else:
            pass
        return obj, created


class CardManager(models.Manager):
    def all(self, *args, **kwargs): # ModelKlass.objects.all() --> ModelKlass.objects.filter(active=True)
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = Customer.get(customer_id=billing_profile.customer_id)
            # stripe_card_response = customer.sources.create(source=token)
            new_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = customer.id,
                    brand = self.brand,
                    country = self.country,
                    exp_month = self.exp_month,
                    exp_year = self.exp_year,
                    last4 = self.last4
                )
            new_card.save()
            return new_card
        return None





# stripe.Charge.create(
#   amount = int(order_obj.total * 100),
#   currency = "usd",
#   customer =  BillingProfile.objects.filter(email='hello@teamcfe.com').first().stripe_id,
#   source = Card.objects.filter(billing_profile__email='hello@teamcfe.com').first().stripe_id, # obtained with Stripe.js
#   description="Charge for elijah.martin@example.com"
# )

class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj, card=None): # Charge.objects.do()
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True) # card_obj.billing_profile
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available"
        c = stripe.Charge.create(
              amount = int(order_obj.total * 100), # 39.19 --> 3919
              currency = "usd",
              customer =  billing_profile.customer_id,
              source = card_obj.stripe_id,
              metadata={"order_id":order_obj.order_id},
            )
        new_charge_obj = self.model(
                billing_profile = billing_profile,
                stripe_id = c.id,
                paid = c.paid,
                refunded = c.refunded,
                outcome = c.outcome,
                outcome_type = c.outcome['type'],
                seller_message = c.outcome.get('seller_message'),
                risk_level = c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message




