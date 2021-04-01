from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    FormMixin,
    UpdateView
)
from django.views.generic.edit import FormMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
import datetime
from sweetify.views import SweetifySuccessMixin
import sweetify
from django.utils.translation import ugettext_lazy as _
from angalabiri.causes.models import Cause
from category.models import Category, Tag

User = get_user_model()

# Create your views here.
class CauseList(ListView):
    model = Cause
    template_name = 'pages/causes.html'
    ordering = ['title', '-end_date']
    queryset = Cause.objects.all()
    context_object_name = 'causes'
    allow_empty = True
    paginate_by = 20
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        tags = Tag.objects.all().filter(categories__title__iexact="Cause")
        context['tags'] = tags
        return context


class CauseDetail(DetailView):
    model = Cause
    template_name = 'pages/cause-detail.html'
    ordering = ['title', '-end_date']
    allow_empty = True
    queryset = Cause.objects.all()
    # context_object_name = 'cause'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all().filter(categories__title__iexact="Cause")
        context['tags'] = tags
        return context
