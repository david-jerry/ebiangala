from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SuggestionConfig(AppConfig):
    name = 'angalabiri.suggestion'
    verbose_name = _("Suggestion")

    def ready(self):
        # story_model = apps.get_model("etopoenergy.blog", "etopoenergy.blog.models.Post")
        # secretballot.enable_voting_on(story_model)
        try:
            import angalabiri.suggestion.signals  # noqa F401
        except ImportError:
            pass
