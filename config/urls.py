from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from config.sitemaps import StaticViewSitemap

from go3xpress.core.views import switch_language, item_detail, verify_tracking, verify_email, home, delivery_list

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = i18n_patterns(
    path("", view=home, name="home"),
    path(
        "search/", view=delivery_list, name="search"
    ),
    path(
        "delivery/<tracking>/", view=item_detail, name="item_detail"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', include('admin_honeypot.urls', 'admin_honeypot')),
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ADMIN_DOC_URL, include("django.contrib.admindocs.urls")),

    # User management
    path("users/", include("go3xpress.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),

    # Your stuff: custom urls includes go here
    path('rosetta/', include('rosetta.urls')),
 ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path("sitemap.xml/", sitemap, kwargs={"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += i18n_patterns(
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
        path("__reload__/", include("django_browser_reload.urls")),
    )
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

urlpatterns += [
        path("<str:language>/<str:url>/", view=switch_language, name="language"),
        path("tracking/", view=verify_tracking, name="verify_tracking"),
        path("email/", view=verify_email, name="verify_email"),
]
