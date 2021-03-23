from dal import autocomplete
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Post
User = get_user_model()


class PostAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Post.objects.none()

        qs = Post.objects.all()

        if self.q:
            lookups = (
                Q(title__istartswith=self.q)
                | Q(categories__istartswith=self.q)
                | Q(author__istartswith=self.q)
                | Q(tags__istartswith=self.q)
            )
            qs = qs.filter(lookups)

        return qs
