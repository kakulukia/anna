from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

from application.views import render_flatpage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin', RedirectView.as_view(url='/admin/')),
    path('', include('application.urls')),
    path('<url>', render_flatpage),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
