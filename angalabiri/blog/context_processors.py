from django.shortcuts import get_object_or_404, redirect, render

from .models import Comment, Post


def recent_posts(request):
    return {
        "recent_posts": Post.objects.filter(featured=True).order_by("-pub_date")[0:2],
    }
