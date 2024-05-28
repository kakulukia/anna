from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path('search', views.search, name="search"),
    path("termine", views.appointments, name="appointments"),
    path("forum", views.forum, name="forum"),
    path("datenschutz", views.data_security, name="datenschutz"),
    path("profile/", views.profile, name="profile"),
    path("reset-password", views.reset_password, name="reset-password"),
    path("logout/", views.signout, name="logout"),
    # Test path for checking the browser, IP-address, and device info of the user
    path("browser/", views.get_browser_info, name="browser"),
    path("media/<media_id>/done", views.mark_as_done, name="mark-as-done"),
    path("device/<int:device_id>/delete", views.delete_user_device, name="delete_device"),
    # Path to All trainings Page
    path("kurse/", views.all_trainings, name="trainings"),
    # Path to (Single training - with all modules) Page
    path("kurse/<int:training_id>/kapitel/", views.all_modules, name="all_modules"),
    path("kurse/<int:training_id>/", views.resume_all_modules, name="resume_all_modules"),
    # Path to (Single training - with single module - with all videos) Page
    path("kurse/<int:training_id>/kapitel/<int:module_id>/lektionen/", views.media, name="media"),
    # Path to (Single training - with single module - with single media) Page
    path(
        "kurse/<int:training_id>/kapitel/<int:module_id>/lektionen/<int:media_id>/",
        views.single_media,
        name="single_media",
    ),
    path(
        "lektion/<int:media_id>/",
        views.single_media_advertising,
        name="single_media_advertising",
    ),
    path("progress/", views.progress, name="progress"),
    path("progress/customer/<id>/trainings/", views.progress_trainings, name="progress-training"),
    path(
        "progress/customer/<id>/trainings/<training_id>/modules/",
        views.progress_modules,
        name="progress-module",
    ),
    path(
        "admin_copy_media/<int:media_id>/",
        views.copy_media,
        name="copy_media",
    ),
    path(
        "admin_copy_media/<int:media_id>/<int:module_id>",
        views.copy_media,
    ),
]
