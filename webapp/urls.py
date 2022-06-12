from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from application.views import render_flatpage

urlpatterns = [
    path("admin/", admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path("admin", RedirectView.as_view(url="/admin/")),
    path("", include("application.urls")),
    path("<url>", render_flatpage),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
