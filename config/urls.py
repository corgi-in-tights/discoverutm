from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="pages/home.html", content_type="text/html"),
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="pages/contact.html", content_type="text/html"),
    ),
    path("u/", include("discovery.urls")),
    path("post/", include("posts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("account/", include("allauth.urls")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("posts.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static("robots.txt", document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
