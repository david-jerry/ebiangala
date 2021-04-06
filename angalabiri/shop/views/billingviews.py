# from django.conf import settings
# from django.http import JsonResponse, HttpResponse
# from django.shortcuts import render, redirect
# from django.utils.http import is_safe_url


# from paystackapi.paystack import Paystack

# from paystackapi.customer import Customer

# from paystackapi.verification import Verification

# paystack_secret_key = settings.PAYSTACK_SECRET_KEY
# paystack_public_key = settings.PAYSTACK_PUBLIC_KEY

# paystack = Paystack(secret_key=paystack_secret_key)


# # import stripe
# # STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_cu1lQmcg1OLffhLvYrSCp5XE")
# # STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_PrV61avxnHaWIYZEeiYTTVMZ')
# # stripe.api_key = STRIPE_SECRET_KEY


# from angalabiri.shop.models.billingmodels import BillingProfile, Card

# def payment_method_view(request):
#     #next_url =
#     # if request.user.is_authenticated():
#     #     billing_profile = request.user.billingprofile
#     #     my_customer_id = billing_profile.customer_id

#     billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#     if not billing_profile:
#         return redirect("/shop/cart")
#     next_url = None
#     next_ = request.GET.get('next')
#     if is_safe_url(next_, request.get_host()):
#         next_url = next_
#     return render(request, 'shop/billing/payment-method.html', {"publish_key": paystack_public_key, "next_url": next_url})


# def payment_method_createview(request):
#     if request.method == "POST" and request.is_ajax():
#         billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#         if not billing_profile:
#             return HttpResponse({"message": "Cannot find this user"}, status_code=401)
#         token = request.POST.get("token")
#         if token is not None:
#             new_card_obj = Card.objects.add_new(billing_profile, token)
#         return JsonResponse({"message": "Success! Your card was added."})
#     return HttpResponse("error", status_code=401)


from django.conf import settings
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from paystackapi.customer import Customer

paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack_public_key = settings.PAYSTACK_PUBLIC_KEY

paystack = Paystack(secret_key=paystack_secret_key)

from angalabiri.shop.models.ordermodels import Order
from django.shortcuts import get_object_or_404, redirect, render


def payment_process(request):
    order_id = request.session.get["order_id"]
    order = get_object_or_404(Order, id=order_id)
    paystack_key = paystack_public_key

    if request.method == "POST":
        transaction = Transaction.initialize(
            reference=f"ANGALABIRI_REF_ORDER_{order_id}",
            email=order.email,
            amount="{:.2f}".format(order.get_total_cost()) * 100,
        )
        if transaction.is_success:
            order.paid = True
            order.transaction_id = transaction.id
            order.save()
            return redirect('shop:payment-done')
        else:
            return redirect('shop:payment-failed')
    return render(request, 'shop/billing/payment.html', {'order': order, 'paystack_key': paystack_key})


def payment_done(request):
    return render(request, 'shop/billing/payment-done.html')


def payment_failed(request):
    return render(request, 'shop/billing/payment-failed.html')
