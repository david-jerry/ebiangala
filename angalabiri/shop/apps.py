from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ShopConfig(AppConfig):
    name = 'angalabiri.shop'
    verbose_name = _("Shops")

    def ready(self):
        # story_model = apps.get_model("etopoenergy.blog", "etopoenergy.blog.models.Post")
        # secretballot.enable_voting_on(story_model)
        try:
            import angalabiri.shop.signals  # noqa F401
        except ImportError:
            pass
