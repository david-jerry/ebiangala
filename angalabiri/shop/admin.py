from django.contrib import admin
from angalabiri.shop.models.addressmodels import Address

from angalabiri.shop.models.billingmodels import BillingProfile, Card, Charge
from angalabiri.shop.models.ordermodels import Order, ProductPurchase
from angalabiri.shop.models.productmodels import Product, ProductFile, ProductImage, ProductVariation
from angalabiri.shop.models.cartmodels import Cart

# Register your models here.
class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1



class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'is_digital']
    inlines = [ProductFileInline, ProductImageInline, ProductVariationInline]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)


admin.site.register(Order)

admin.site.register(ProductPurchase)

# admin.site.register(Cart)

admin.site.register(BillingProfile)

admin.site.register(Card)

admin.site.register(Charge)

admin.site.register(Address)