import os
from wsgiref.util import FileWrapper # this used in django
from mimetypes import guess_type

from django.conf import settings
# from orders.models import ProductPurchase
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category, Tag
from angalabiri.shop.forms.cartform import CartAddProductForm
from angalabiri.shop.models.productmodels import Product, ProductVariation, ProductFile, ProductImage
# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = "shop/products/list.html"
    ordering = ["title"]
    queryset = Product.objects.all()
    context_object_name = "products"
    allow_empty = True
    paginate_by = 20
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        tags = Tag.objects.all().filter(categories__title__iexact="Shop")
        context["tags"] = tags
        return context

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, draft=False)
    tags = Tag.objects.all().filter(categories__title__iexact="Shop")
    cart_form = CartAddProductForm()
    return render(request, 'shop/products/detail.html', {'tags':tags, 'cart_form':cart_form, 'product':product})




# class ProductDetail(DetailView):
#     model = Product
#     template_name = "shop/products/detail.html"
#     ordering = ["title"]
#     queryset = Product.objects.all()
#     context_object_name = "product"
#     allow_empty = True
#     paginate_by = 20
#     slug_field = "slug"
#     slug_url_kwarg = "slug"

#     def get_object(self, *args, **kwargs):
#         request = self.request
#         slug = self.kwargs.get("slug")
#         try:
#             product = Product.objects.get(slug=slug, draft=False)
#         except Product.DoesNotExist:
#             raise Http404("Not Found...")
#         except Product.MultipleObjectsReturned:
#             qs = Product.objects.filter(slug=slug, draft=False)
#             product = qs.first()
#         except:
#             raise Http404("Nothing to show")
#         return product

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         tags = Tag.objects.all()
#         context["tags"] = tags
#         categories = Category.objects.all()
#         context["categories"] = categories
#         return context


class ProductDownload(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("Download not found")
        download_obj = downloads_qs.first()
        # permission checks

        can_download = False
        user_ready  = True
        if download_obj.user_required:
            if not request.user.is_authenticated():
                user_ready = False

        purchased_products = Product.objects.none()
        if download_obj.free:
            can_download = True
            user_ready = True
        else:
            # not free
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item")
            return redirect(download_obj.get_default_url())

        aws_filepath = download_obj.generate_download_url()
        print(aws_filepath)
        return HttpResponseRedirect(aws_filepath)
