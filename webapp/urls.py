from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from application.admin import clone_user
from application.views import render_flatpage
from users.views import create_or_update_lead_webhook


class PasswordResetView(auth_views.PasswordResetView):
    from_email = "neuespasswort@liebendgern.de"


urlpatterns = [
    path("admin/clone-user/<int:user_id>/", clone_user, name="clone-user"),
    path("admin/", admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path("admin", RedirectView.as_view(url="/admin/")),
    path("", include("application.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('', include('django_sso.sso_gateway.urls')),
    path('api/lead-webhook/', create_or_update_lead_webhook),

    path("password_reset/", PasswordResetView.as_view(), name="admin_password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),


    path("<url>", render_flatpage),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
