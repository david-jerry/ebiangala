from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        # All posts
        return super().get_queryset().filter(draft=False)

    def featured(self):
        # All posts
        return super().get_queryset().filter(featured=True)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-created", "-updated")

    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        recent_cart_data = recent.cart_data()
        shipped = recent.not_refunded().by_status(status='shipped')
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status='paid')
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data':recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid': paid,
            'paid_data': paid_data
        }
        return data

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7  # days_ago_start = 49
        days_ago_end = days_ago_start - (number_of_weeks * 7) #days_ago_end = 49 - 14 = 35
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end) 
        return self.by_range(start_date, end_date=end_date)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated__gte=start_date)
        return self.filter(updated__gte=start_date).filter(updated__lte=end_date)

    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(updated__day__gte=now.day)

    def totals_data(self):
        return self.aggregate(Sum("total"), Avg("total"))

    def cart_data(self):
        return self.aggregate(
                        Sum("cart__products__price"), 
                        Avg("cart__products__price"), 
                        Count("cart__products")
                                    )

    def by_status(self, status="shipped"):
        return self.filter(status=status)

    def not_refunded(self):
        return self.exclude(status='refunded')

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
                billing_profile=billing_profile, 
                cart=cart_obj, 
                active=True, 
                status='created'
            )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile, 
                    cart=cart_obj)
            created = True
        return obj, created


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class ProductPurchaseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)

    def digital(self):
        return self.filter(product__is_digital=True)

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)



class ProductPurchaseManager(models.Manager):
    def get_queryset(self):
        return ProductPurchaseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def digital(self):
        return self.get_queryset().active().digital()

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def products_by_id(self, request):
        qs = self.by_request(request).digital()
        ids_ = [x.product.id for x in qs]
        return ids_

    def products_by_request(self, request):
        ids_ = self.products_by_id(request)
        products_qs = Product.objects.filter(id__in=ids_).distinct()
        return products_qs








class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated():
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                            user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                                            email=guest_email_obj.email)
        else:
            pass
        return obj, created


class CardManager(models.Manager):
    def all(self, *args, **kwargs): # ModelKlass.objects.all() --> ModelKlass.objects.filter(active=True)
        return self.get_queryset().filter(active=True)

    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            stripe_card_response = customer.sources.create(source=token)
            new_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = stripe_card_response.id,
                    brand = stripe_card_response.brand,
                    country = stripe_card_response.country,
                    exp_month = stripe_card_response.exp_month,
                    exp_year = stripe_card_response.exp_year,
                    last4 = stripe_card_response.last4
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




