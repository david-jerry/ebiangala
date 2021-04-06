from django.contrib import admin

from angalabiri.shop.models.ordermodels import Order, OrderItem
from angalabiri.shop.models.productmodels import (
    Product,
    ProductFile,
    ProductImage,
    ProductVariation,
)

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
    list_display = ["__str__", "slug", "is_digital"]
    inlines = [ProductFileInline, ProductImageInline, ProductVariationInline]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "created",
        "modified",
    ]
    list_filter = ["paid", "created", "modified"]
    inlines = [OrderItemInline]


# admin.site.register(Cart)

