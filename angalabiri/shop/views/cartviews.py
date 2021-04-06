from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

# from users.forms import LoginForm

# from angalabiri.shop.forms.addressforms import AddressCheckoutForm
from angalabiri.shop.forms.cartform import CartAddProductForm
# from angalabiri.shop.models.addressmodels import Address

# from angalabiri.shop.models.billingmodels import BillingProfile
from angalabiri.shop.models.ordermodels import Order
from angalabiri.shop.models.productmodels import Product
from angalabiri.shop.cart import Cart


# import stripe
# STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_cu1lQmcg1OLffhLvYrSCp5XE")
# STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_PrV61avxnHaWIYZEeiYTTVMZ')
# stripe.api_key = STRIPE_SECRET_KEY
from paystackapi.paystack import Paystack
from paystackapi.customer import Customer
from paystackapi.verification import Verification

paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
paystack = Paystack(secret_key=paystack_secret_key)

from allauth.account.forms import LoginForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('shop:cart')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update':True})
    return render(request, 'shop/carts/home.html', {'cart':cart})























# def cart_detail_api_view(request):
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     products = [{
#             "id": x.id,
#             "url": x.get_absolute_url(),
#             "name": x.name,
#             "price": x.price
#             }
#             for x in cart_obj.products.all()]
#     cart_data  = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
#     return JsonResponse(cart_data)

# def cart_home(request):
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     return render(request, "shop/carts/home.html", {"cart": cart_obj})


# def cart_update(request):
#     product_id = request.POST.get('product_id')

#     if product_id is not None:
#         try:
#             product_obj = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             print("Show message to user, product is gone?")
#             return redirect("shop:cart")
#         cart_obj, new_obj = Cart.objects.new_or_get(request)
#         if product_obj in cart_obj.products.all():
#             cart_obj.products.remove(product_obj)
#             added = False
#         else:
#             cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
#             added = True
#         request.session['cart_items'] = cart_obj.products.count()
#         # return redirect(product_obj.get_absolute_url())
#         if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
#             print("Ajax request")
#             json_data = {
#                 "added": added,
#                 "removed": not added,
#                 "cartItemCount": cart_obj.products.count()
#             }
#             return JsonResponse(json_data, status=200) # HttpResponse
#             # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
#     return redirect("shop:cart")



# def checkout_home(request):
#     cart_obj, cart_created = Cart.objects.new_or_get(request)
#     order_obj = None
#     if cart_created or cart_obj.products.count() == 0:
#         return redirect("shop:cart")

#     login_form = LoginForm(request=request)
#     # guest_form = GuestForm(request=request)
#     address_form = AddressCheckoutForm()
#     billing_address_id = request.session.get("billing_address_id", None)

#     shipping_address_required = not cart_obj.is_digital


#     shipping_address_id = request.session.get("shipping_address_id", None)

#     billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#     address_qs = None
#     has_card = False
#     if billing_profile is not None:
#         if request.user.is_authenticated():
#             address_qs = Address.objects.filter(billing_profile=billing_profile)
#         order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
#         if shipping_address_id:
#             order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
#             del request.session["shipping_address_id"]
#         if billing_address_id:
#             order_obj.billing_address = Address.objects.get(id=billing_address_id)
#             del request.session["billing_address_id"]
#         if billing_address_id or shipping_address_id:
#             order_obj.save()
#         has_card = billing_profile.has_card

#     if request.method == "POST":
#         "check that order is done"
#         is_prepared = order_obj.check_done()
#         if is_prepared:
#             did_charge, crg_msg = billing_profile.charge(order_obj)
#             if did_charge:
#                 order_obj.mark_paid() # sort a signal for us
#                 request.session['cart_items'] = 0
#                 del request.session['cart_id']
#                 if not billing_profile.user:
#                     '''
#                     is this the best spot?
#                     '''
#                     billing_profile.set_cards_inactive()
#                 return redirect("cart:success")
#             else:
#                 print(crg_msg)
#                 return redirect("cart:checkout")
#     context = {
#         "object": order_obj,
#         "billing_profile": billing_profile,
#         "login_form": login_form,
#         "address_form": address_form,
#         "address_qs": address_qs,
#         "has_card": has_card,
#         "publish_key": PAYSTACK_PUBLIC_KEY,
#         "shipping_address_required": shipping_address_required,
#     }
#     return render(request, "shop/carts/checkout.html", context)







# def checkout_done_view(request):
#     return render(request, "shop/carts/checkout-done.html", {})






