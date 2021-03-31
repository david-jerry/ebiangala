from django.views.generic import TemplateView, RedirectView
from django.urls import path
from angalabiri.shop.views.productviews import ProductList, ProductDetail, ProductDownload
from angalabiri.shop.views.cartviews import cart_home, cart_update, checkout_home, checkout_done_view, cart_detail_api_view
from angalabiri.shop.views.orderviews import OrderListView, OrderDetailView, VerifyOwnership, OrderLibraryView
from angalabiri.shop.views.billingviews import payment_method_view, payment_method_createview
from angalabiri.shop.views.addressviews import AddressCreateView, AddressListView, AddressUpdateView, checkout_address_create_view, checkout_address_reuse_view

app_name = "shop"

urlpatterns = [
    path('', ProductList.as_view(), name='list'),
    path('<slug>/', ProductDetail.as_view(), name='detail'),
    path('<slug>/<int:pk>/', ProductDownload.as_view(), name='download'),


    path('cart/', cart_home, name='home'),
    path('cart/api/', cart_detail_api_view, name='api-cart'),
    path('cart/checkout/success/', checkout_done_view, name='success'),
    path('cart/checkout/', checkout_home, name='checkout'),
    path('cart/update/', cart_update, name='update'),


    path('order/', OrderListView.as_view(), name='orders'),
    path('order/endpoint/verify/ownership/', VerifyOwnership.as_view(), name='verify-ownership'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order'),
    path('order/library/', OrderLibraryView.as_view(), name='library'),


    path('address/', RedirectView.as_view(url='/addresses')),
    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/create/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/<int:pk>/', AddressUpdateView.as_view(), name='address-update'),


    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),


    path('billing/payment-method/', payment_method_view, name='billing-payment-method'),
    path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
]
