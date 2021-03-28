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
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView
from django.views.generic.edit import FormMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
import datetime
from sweetify.views import SweetifySuccessMixin
import sweetify
from django.utils.translation import ugettext_lazy as _
from angalabiri.suggestion.models import Suggestion
from angalabiri.suggestion.forms import SuggestionForm

User = get_user_model()

# Create your views here.
class SuggestionList(ListView):
    model = Suggestion
    template_name = "pages/suggestion/list.html"
    ordering = ["title", "-pub_date"]
    queryset = Suggestion.objects.all_suggestion()
    context_object_name = "objs"
    allow_empty = True
    paginate_by = 20
    slug_field = "slug"
    slug_url_kwarg = "slug"

class SuggestionDetail(DetailView):
    model = Suggestion
    template_name = "pages/suggestion/detail.html"
    ordering = ["title", "pub_date"]
    allow_empty = True
    queryset = Suggestion.objects.all_suggestion()
    context_object_name = 'obj'
    slug_field = "slug"
    slug_url_kwarg = "slug"

class SuggestionCreate(CreateView):
    model = Suggestion
    template_name = "pages/suggestion/list.html"
    form_class = SuggestionForm()

    def get_success_url(self):
        return reverse("suggestion:detail", kwargs={"slug": self.object.slug})


    def form_valid(self, form):

        return super().form_valid(form)
