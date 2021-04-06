from django.views.generic import TemplateView, RedirectView
from django.urls import path
from angalabiri.shop.views.productviews import (
    ProductList,
    product_detail,
    ProductDownload,
)

# from angalabiri.shop.views.cartviews import cart_home, cart_update, checkout_home, checkout_done_view, cart_detail_api_view
from angalabiri.shop.views.cartviews import cart_add, cart_remove, cart_detail
from angalabiri.shop.views.orderviews import (
    OrderListView,
    OrderCreate,
    OrderDetailView,
)  # , VerifyOwnership, OrderLibraryView
from angalabiri.shop.views.billingviews import (
    payment_process,
    payment_done,
    payment_failed
)
# from angalabiri.shop.views.addressviews import (
#     AddressCreateView,
#     AddressListView,
#     AddressUpdateView,
#     checkout_address_create_view,
#     checkout_address_reuse_view,
# )

app_name = "shop"

urlpatterns = [
    path(
        "", TemplateView.as_view(template_name="shop/products/home.html"), name="home"
    ),
    path("products/", ProductList.as_view(), name="list"),
    path("products/<slug>/<int:id>", product_detail, name="detail"),
    path("products/<slug>/<int:pk>/", ProductDownload.as_view(), name="download"),
    path("cart/", cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", cart_add, name="add"),
    path("cart/remove/<int:product_id>/", cart_remove, name="remove"),
    path("order/", OrderListView.as_view(), name="orders"),
    path("order/create/", OrderCreate, name="order-create"),
    path("order/<int:order_id>/", OrderDetailView.as_view(), name="order"),
    # path('order/library/', OrderLibraryView.as_view(), name='library'),
    # path("address/", RedirectView.as_view(url="/addresses")),
    # path("addresses/", AddressListView.as_view(), name="addresses"),
    # path("addresses/create/", AddressCreateView.as_view(), name="address-create"),
    # path("addresses/<int:pk>/", AddressUpdateView.as_view(), name="address-update"),
    # path(
    #     "checkout/address/create/",
    #     checkout_address_create_view,
    #     name="checkout_address_create",
    # ),
    # path(
    #     "checkout/address/reuse/",
    #     checkout_address_reuse_view,
    #     name="checkout_address_reuse",
    # ),
    path("billing/payment-method/", payment_process, name="payment_method"),
    path("billing/payment-done/", payment_done, name="payment_done"),
    path("billing/payment-canceled/", payment_failed, name="payment_failed"),
    # path(
    #     "billing/payment-method/create/",
    #     payment_method_createview,
    #     name="billing-payment-method-endpoint",
    # ),
]
