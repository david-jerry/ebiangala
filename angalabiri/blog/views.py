try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

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
from angalabiri.blog.models import Post, Comment
from angalabiri.blog.forms import CommentForm
from category.models import Category, Tag
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

# Create your views here.
class PostList(ListView):
    model = Post
    template_name = "pages/blog/list.html"
    ordering = ["title", "-pub_date"]
    queryset = Post.objects.all_posts()
    context_object_name = "posts"
    allow_empty = True
    paginate_by = 20
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        tags = Tag.objects.all()
        context["tags"] = tags
        return context


# class PostDetail(DetailView, FormMixin):
#     model = Post
#     template_name = "pages/blog/detail.html"
#     ordering = ["title", "pub_date"]
#     allow_empty = True
#     form_class = CommentForm
#     queryset = Post.objects.all_posts()
#     context_object_name = 'post'
#     slug_field = "slug"
#     slug_url_kwarg = "slug"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         tags = Tag.objects.all()
#         post = self.object
#         comments = post.comments.filter(active=True)
#         share_string = quote_plus(post.content)
#         context["tags"] = tags
#         context["comments"] = comments
#         context["share_string"] = share_string
#         return context

#     def get_success_url(self):
#         return reverse("blog:detail", kwargs={"slug": self.object.slug})

#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         instance = self
#         print (instance)
#         initial_data = {
#             "content_type": instance.get_content_type,
#             "object_id": instance.id
#         }
#         if self.request.user.is_authenticated:
#             c_type = form.cleaned_data.get("content_type")
#             content_type = ContentType.objects.get(model=c_type)
#             obj_id = form.cleaned_data.get("object_id")
#             content_data = form.cleaned_data.get("text")
#             parent_obj = None
#             author = self.request.user
#             email = self.request.user.email
#             try:
#                 parent_id = int(self.request.POST.get("parent_id"))
#             except:
#                 parent_id = None

#             if parent_id:
#                 parent_qs = Comment.objects.filter(id=parent_id)
#                 if parent_qs.exists() and parent_qs.count() == 1:
#                     parent_obj = parent_qs.first()

#             new_comment, created = Comment.objects.get_or_create(
#                 author=author,
#                 email=email,
#                 content_type=content_type,
#                 object_id=obj_id,
#                 content=content_data,
#                 parent=parent_obj,
#             )
#             return HttpResponseRedirect(content_type.get_absolute_url())
#         return super().form_valid(form)


def PostDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    tags = Tag.objects.all()
    new_comment = None
    if request.method == "POST" and request.is_ajax():
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return JsonResponse({"success":True}, status=200)
    else:
        comment_form = CommentForm()
        return JsonResponse({"success":False}, status=400)

    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "form": comment_form,
        "tags": tags
    }
    return render(request, "pages/blog/detail.html", context)


    # share_string = quote_plus(instance.content)
    # initial_data = {"content_type": instance.get_content_type, "object_id": instance.id}
    # form = CommentForm(request.POST or None, initial=initial_data)
    # if form.is_valid() and request.user.is_authenticated:
    #     c_type = form.cleaned_data.get("content_type")
    #     content_type = ContentType.objects.get(model=c_type)
    #     obj_id = form.cleaned_data.get("object_id")
    #     content_data = form.cleaned_data.get("content")
    #     parent_obj = None
    #     author = self.request.user
    #     email = self.request.user.email
    #     try:
    #         parent_id = int(request.POST.get("parent_id"))
    #     except:
    #         parent_id = None

    #     if parent_id:
    #         parent_qs = Comment.objects.filter(id=parent_id)
    #         if parent_qs.exists() and parent_qs.count() == 1:
    #             parent_obj = parent_qs.first()

    #     new_comment, created = Comment.objects.get_or_create(
    #         author=author,
    #         email=email,
    #         content_type=content_type,
    #         object_id=obj_id,
    #         content=content_data,
    #         parent=parent_obj,
    #     )
    #     return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    # comments = instance.comments
    # tags = Tag.objects.all()
    # context = {
    #     "title": instance.title,
    #     "post": instance,
    #     "share_string": share_string,
    #     "comments": comments,
    #     "comment_form": form,
    #     "tags": tags,
    # }
    # return render(request, "pages/blog/detail.html", context)


class TagDetail(DetailView):
    model = Tag
    template_name = "pages/blog/tags.html"
    ordering = ["title", "pub_date"]
    allow_empty = True
    queryset = Post.objects.all_posts()
    context_object_name = "tag"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        context["tags"] = tags
        return context
