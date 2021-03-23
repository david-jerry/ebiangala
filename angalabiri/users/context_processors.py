from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count

from .models import User


def all_citizen(request):
    return {
        "all_citizen": User.objects.all().order_by("-id").count(),
    }

def all_chiefs(request):
    return {
        "all_chiefs": User.objects.all_cheifs().order_by("-id").count(),
    }

def all_females(request):
    return {
        "all_females": User.objects.all_female().count(),
    }

def all_males(request):
    return {
        "all_males": User.objects.all_male().count(),
    }
