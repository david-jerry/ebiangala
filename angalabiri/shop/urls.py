from django.urls import path
from angalabiri.shop.views.productviews import ProductList, ProductDetail, ProductDownload
from angalabiri.shop.views.cartviews import cart_home, cart_update, checkout_home, checkout_done_view
from angalabiri.shop.views.orderviews import ListView, DetailView, VerifyOwnership

app_name = "shop"

urlpatterns = [
    path('', ProductList.as_view(), name='list'),
    path('<slug>/', ProductDetail.as_view(), name='detail'),
    path('<slug>/<int:pk>/', ProductDownload.as_view(), name='download'),


    path('cart/', cart_home, name='home'),
    path('cart/checkout/success/', checkout_done_view, name='success'),
    path('cart/checkout/', checkout_home, name='checkout'),
    path('cart/update/', cart_update, name='update'),


    url('order/', ListView.as_view(), name='orders'),
    url('order/endpoint/verify/ownership/', VerifyOwnership.as_view(), name='verify-ownership'),
    url('order/<order_id>/', DetailView.as_view(), name='order'),

]
