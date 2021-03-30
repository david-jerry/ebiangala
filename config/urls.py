from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls

from angalabiri.users.autocomplete import UsersAutocomplete
from config.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}


def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


sentry_debug = [
    path("sentry-debug/", trigger_error),
]
auto_complete_linnks = [
    path("user-autocomplete/", UsersAutocomplete.as_view(), name="user-autocomplete"),
]
admin_pages = [
    # Django Admin, use {% url 'admin:index' %}
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("jet/", include("jet.urls", namespace="jet")),
    path("jet/dashboard/", include("jet.dashboard.urls", namespace="jet-dashboard")),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ADMIN_DOC_URL, include("django.contrib.admindocs.urls")),
]

static_pages = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("the-king/", TemplateView.as_view(template_name="pages/hrh.html"), name="hrh"),
    path("the-royal-family/", TemplateView.as_view(template_name="pages/family.html"), name="fam"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
]

apps_pages = [
    # User management
    path("users/", include("angalabiri.users.urls", namespace="users")),
    path("blogs/", include("angalabiri.blog.urls", namespace="blog")),
    path("suggestion/", include("angalabiri.suggestion.urls", namespace="suggestion")),
    path("shop/", include("angalabiri.shop.urls", namespace="shop")),
    path("cause/", include("angalabiri.causes.urls", namespace="cause")),
    path("accounts/", include("allauth.urls")),
    path("comment/", include('comment.urls')),
    # Your stuff: custom urls includes go here
]

custom_pages = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]
urlpatterns = (
    sentry_debug
    + auto_complete_linnks
    + static_pages
    + admin_pages
    + apps_pages
    + custom_pages
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    # Documentation of API
    path("api/docs/", include_docs_urls(title="Angalabir API")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = "Angalabiri Portal"
admin.site.site_title = "Angalabiri Portal"
admin.site.index_title = "Welcome to Angalabiri Community Portal"
