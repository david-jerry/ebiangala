from django.shortcuts import get_object_or_404, redirect, render

from .models import Cause
from django.db.models import Sum

def featured_causes(request):
    return {
        "featured_causes": Cause.objects.all().order_by("-end_date")[0:6],
    }


def richest_causes(request):
    return {
        "richest_causes": Cause.objects.all().aggregate(Sum("tt_amount")),
    }
