from django.shortcuts import get_object_or_404, redirect, render

from angalabiri.shop.models.productmodels import Product
from category.models import Category, Tag
from angalabiri.shop.cart import Cart

def featured_products(request):
    return {
        "featured_products": Product.objects.filter(featured=True).order_by("-created")[0:4],
    }

def new_arrivals(request):
    return {
        "new_arrivals": Product.objects.filter(old_stock=False).order_by("-modified")[0:4],
    }

def all_cat(request):
    return {
        "all_cat": Tag.objects.all().filter(categories__title__iexact="shop").order_by("title"),
    }


def cart(request):
    return {'cart':Cart(request)}