# Generated by Django 3.1.7 on 2021-04-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210403_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paystack_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
