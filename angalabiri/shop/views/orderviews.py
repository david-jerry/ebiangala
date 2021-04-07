from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.views.generic import View, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect, render

# from angalabiri.shop.models.billingmodels import BillingProfile
from angalabiri.shop.models.ordermodels import Order, OrderItem
from angalabiri.shop.forms.orderforms import OrderCreateForm
from angalabiri.shop.cart import Cart
from django.contrib import messages
from angalabiri.shop.tasks import order_created
from django.urls import reverse
# from paystackapi.paystack import Paystack
# from paystackapi.transaction import Transaction
# from paystackapi.customer import Customer
import random
import string
from django.conf import settings

paystack_secret_key = settings.PAYSTACK_SECRET_KEY
paystack_public_key = settings.PAYSTACK_PUBLIC_KEY

# paystack = Paystack(secret_key=paystack_secret_key)


def OrderCreate(request):
    rand = ''.join(
        [random.choice(
            string.ascii_letters + string.digits) for n in range(16)])
    paystack_key = paystack_public_key
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            request.session["order_id"] = order.id
            # transaction = Transaction.initialize(
            #     reference=rand,
            #     email=current_order.email,
            #     amount="{:.2f}".format(current_order.get_total_cost()) * 100,
            # )
            # Transaction.charge(
            #     reference=transaction.reference,
            #     authorization_code=transaction.authorization_code,
            #     amount=transaction.amount
            # )
            order.paid = True
            order.save()
            order_created.delay(order.id)
            messages.success(
                request, "Order Completed. \n Your order id is: {}".format(order.id)
            )
            # return redirect(reverse("shop:payment_done"))
        else:
            messages.error(
                request, "Order Failed. \n Your order id is: {}".format(order.id)
            )
            # return redirect(reverse('shop:payment_failed'))
            # return render(request, "shop/orders/created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(
        request,
        "shop/orders/create.html",
        {"cart": cart, "form": form, "paystack_key": paystack_key, 'rand': rand},
    )


class OrderListView(LoginRequiredMixin, ListView):
    template_name = "shop/orders/list.html"

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "shop/orders/detail.html"

    def get_object(self):
        # return Order.objects.get(id=self.kwargs.get('id'))
        # return Order.objects.get(slug=self.kwargs.get('slug'))
        qs = Order.objects.by_request(self.request).filter(
            order_id=self.kwargs.get("order_id")
        )
        if qs.count() == 1:
            return qs.first()
        raise Http404


# class OrderLibraryView(LoginRequiredMixin, ListView):
#     template_name = 'shop/orders/library.html'
#     def get_queryset(self):
#         return ProductPurchase.objects.products_by_request(self.request) #.by_request(self.request).digital()


# class VerifyOwnership(View):
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax():
#             data = request.GET
#             product_id = request.GET.get('product_id', None)
#             if product_id is not None:
#                 product_id = int(product_id)
#                 ownership_ids = ProductPurchase.objects.products_by_id(request)
#                 if product_id in ownership_ids:
#                     return JsonResponse({'owner': True})
#             return JsonResponse({'owner': False})
#         raise Http404
