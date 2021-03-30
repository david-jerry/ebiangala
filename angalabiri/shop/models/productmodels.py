import random
import os
import math
import datetime
from decimal import Decimal
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from category.models import Category, Tag
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    GenericIPAddressField,
    ImageField,
    IntegerField,
    IPAddressField,
    ManyToManyField,
    OneToOneField,
    Q,
    SlugField,
    URLField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from angalabiri.shop.managers.productmanagers import *
from comment.models import Comment
from django_resized import ResizedImageField
from config.settings.production import PRIVATE_FILE_STORAGE


PRIVATE_FILE_STORAGE
# PRIVATE_FILE_STORAGE = getattr(settings, "PRIVATE_FILE_STORAGE", "angalabiri.utils.storages.PrivateRootS3Boto3Storage")
# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    #print(filename)
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename, 
            final_filename=final_filename
            )



class Product(TimeStampedModel):
    title = CharField(_("Product Name"), max_length=255, null=True, blank=False)
    slug = SlugField(unique=True, null=True, blank=True, max_length=500)
    description = RichTextUploadingField()
    price = DecimalField(decimal_places=2, max_digits=20, default=0.99)
    comments = GenericRelation(Comment)
    added_by = CharField(_("added_by"), max_length=255, null=True, blank=True)
    categories = ManyToManyField("category.Category", help_text="Categorize this Product.")
    tags = ManyToManyField("category.Tag", help_text="Tag this Product.")
    featured = BooleanField(default=False)
    draft = BooleanField(default=False)
    is_digital = BooleanField(default=False)

    objects = ProductManager()

    def __str__(self):
        return str(self.title)

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs

    def get_image_url(self):
        img = self.productimage_set.first()
        if img:
            return img.image.url
        return img

    @property
    def get_related_products_by_tags(self):
        return Product.objects.filter(tags__in=self.tags.all())[0:4]

    @staticmethod
    def autocomplete_search_fields():
        return "title"

    class Meta:
        managed = True
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["title", "-end_date"]

    def get_absolute_url(self):
        return f"/products/{self.slug}"

    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    #id_ = 0
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id_ = 0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "product/{slug}/{id}/".format(slug=slug, id=id_)
    return location + filename #"path/to/filename.mp4"


class ProductFile(TimeStampedModel):
    product = ForeignKey(Product, null=True, on_delete=SET_NULL, blank=False)
    name = CharField(_("Digital Content Name"), null=True, blank=True, max_length=255)
    digi_file = FileField(_("Digital File Upload"), upload_to=upload_product_file_loc, storage=PRIVATE_FILE_STORAGE(),)
    free  = BooleanField(default=False)
    user_required = BooleanField(default=False)

    def __str__(self):
        return str(self.digi_file.name)

    @property
    def display_name(self):
        og_name = get_filename(self.digi_file.name)
        if self.name:
            return self.name
        return og_name

    def get_default_url(self):
        return self.product.get_absolute_url()

    def generate_download_url(self):
        bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
        region = getattr(settings, 'AWS_S3_REGION_NAME')
        access_key = getattr(settings, 'AWS_ACCESS_KEY_ID')
        secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
        if not secret_key or not access_key or not bucket or not region:
            return "/product-not-found/"
        PROTECTED_DIR_NAME = getattr(settings, 'PRIVATE_URL', 'private')
        path = "{base}/{file_path}".format(base=PRIVATE_URL, file_path=str(self.digi_file))
        aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
        file_url = aws_dl_object.generate_url(path, new_filename=self.display_name)
        return file_url

    def get_download_url(self): # detail view
        return reverse("products:download", 
                    kwargs={"slug": self.product.slug, "pk": self.pk}
                )


def upload_product_image_loc(instance, filename):
    slug = instance.product.slug
    #id_ = 0
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id_ = 0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "product/image/{slug}/{id}/".format(slug=slug, id=id_)
    return location + filename #"path/to/filename.mp4"

class ProductVariation(TimeStampedModel):
    product = ForeignKey(Product, related_name="product_variation", on_delete=CASCADE)
    title = CharField(_("Product Variation"),max_length=255, null=True, blank=True)
    price = DecimalField(decimal_places=2, max_digits=20, default=0.99)
    sale_price = DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = BooleanField(default=True)
    inventory = IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.product.title)

    class Meta:
        managed = True
        verbose_name = "Product Variation"
        verbose_name_plural = "Post Variations"
        ordering = ["-created"]

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    # def get_html_price(self):
    # 	if self.sale_price is not None:
    # 		html_text = "<span class='sale-price'>%s</span> <span class='og-price'>%s</span>" %(self.sale_price, self.price)
    # 	else:
    # 		html_text = "<span class='price'>%s</span>" %(self.price)
    # 	return mark_safe(html_text)

    def get_absolute_url(self):
        return f"/products/{self.slug}"

    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"

    def get_title(self):
        return "%s - %s" %(self.product.title, self.title)

class ProductImage(TimeStampedModel):
    product = ForeignKey(product, on_delete=CASCADE)
    image = ResizedImageField(
        _("Upload Product Image"), quality=75, force_format='JPEG', size=[1920, 1148], crop=['middle', 'center'], upload_to=upload_product_image_loc, null=True, blank=True
    )

    def __str__(self):
        return self.product.title

    class Meta:
        managed = True
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["-created"]








