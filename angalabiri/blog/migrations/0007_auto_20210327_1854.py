# Generated by Django 3.1.7 on 2021-03-27 17:54

import angalabiri.blog.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210327_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format='JPEG', keep_meta=True, null=True, quality=75, size=[1920, 1148], upload_to=angalabiri.blog.models.blog_image_path, verbose_name='Upload Post Image'),
        ),
    ]
