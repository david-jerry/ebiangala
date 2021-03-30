from django.shortcuts import get_object_or_404, redirect, render

from .models import Suggestion


def recent_suggestion(request):
    return {
        "recent_suggestion": Suggestion.objects.filter(draft=False).order_by("-pub_date")[0:10],
    }
