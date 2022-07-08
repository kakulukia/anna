from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path('search', views.search, name="search"),
    path("profile/", views.profile, name="profile"),
    path("reset-password", views.reset_password, name="reset-password"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.signout, name="logout"),

    # Test path for checking the browser, IP-address, and device info of the user
    path("browser/", views.get_browser_info, name="browser"),

    path("media/<media_id>/done", views.mark_as_done, name="mark-as-done"),
    path("device/<int:device_id>/delete", views.delete_user_device, name="delete_device"),

    # Path to All trainings Page
    path("kurse/", views.all_trainings, name="trainings"),
    # Path to (Single training - with all modules) Page
    path("kurse/<int:training_id>/kapitel/", views.all_modules, name="all_modules"),
    path("kurse/<int:training_id>/kapitel/", views.all_modules, name="all_modules"),
    path("kurse/<int:training_id>/", views.resume_all_modules, name="resume_all_modules"),
    # Path to (Single training - with single module - with all videos) Page
    path("kurse/<int:training_id>/kapitel/<int:module_id>/lektionen/", views.media, name="media"),
    # Path to (Single training - with single module - with single media) Page
    path("kurse/<int:training_id>/kapitel/<int:module_id>/lektionen/<int:media_id>/",
         views.single_media, name="single_media",
         ),
    path("progress/", views.progress, name="progress"),
    path(
        "progress/customer/<id>/trainings/", views.progress_trainings, name="progress-training"
    ),
    path(
        "progress/customer/<id>/trainings/<training_id>/modules/",
        views.progress_modules,
        name="progress-module",
    ),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
