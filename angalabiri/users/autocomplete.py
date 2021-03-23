from dal import autocomplete
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UsersAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return User.objects.none()

        qs = User.objects.all()

        if self.q:
            lookups = (
                Q(first_name__istartswith=self.q)
                | Q(mid_name__istartswith=self.q)
                | Q(last_name__istartswith=self.q)
            )
            qs = qs.filter(lookups)

        return qs
