from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count

from .models import User


def all_citizen(request):
    return {
        "all_citizen": User.objects.all().order_by("-id").count(),
    }

def all_chiefs(request):
    return {
        "all_chiefs": User.objects.filter(royals__iexact="Chief", is_active=True).order_by("-id").count(),
    }

def all_females(request):
    return {
        "all_females": User.objects.filter(gender__iexact="Female", is_active=True).count(),
    }

def all_males(request):
    return {
        "all_males": User.objects.filter(gender__iexact="Female", is_active=True).count(),
    }
