from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


class MediaInline(admin.StackedInline):
    model = Media
    extra = 1


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    actions = None

    fieldsets = (
        (
            "Infobox",
            {
                "fields": (
                    "name",
                    "description",
                    "thumbnail",
                )
            },
        ),
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    actions = None
    list_display = ['name', 'ordering', 'next']


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['name', 'length', 'next']
    list_filter = ['module']
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        if 'file' in form.changed_data:
            obj.length = ''
        super().save_model(request, obj, form, change)


class AccessInline(admin.StackedInline):
    model = Access
    extra = 1


class DeviceInline(admin.StackedInline):
    model = Device
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [AccessInline, DeviceInline]
    list_display = (
        "email",
        "first_or_username",
        "last_name",
        "start_date",
        "end_date",
        "zoom",
        "option",
    )
    list_display_links = ['email', 'first_or_username']
    list_filter = ["is_superuser", ("zoom_link", admin.EmptyFieldListFilter)]
    verbose_name = "Customer"
    actions = None

    def first_or_username(self, user: User):
        return user.first_name if user.first_name else user.username
    first_or_username.short_description = "Vorname"
    first_or_username.admin_order_field = 'first_name'

    def zoom(self, user: User):
        return bool(user.zoom_link)

    zoom.boolean = True

    def option(self, obj):
        # or anything you prefer e.g. an edit button
        from django.urls import reverse
        from django.utils.html import mark_safe

        if obj.is_superuser or not obj.email:
            return None
        user_id = obj.id
        url = reverse("progress-training", args=[user_id])
        element = f'<a href = "{url}" target="_blank" class = "btn btn-outline-primary">Fortschritt anzeigen</a>'
        return mark_safe(element)

    option.short_description = "Fortschritt"
    readonly_fields = ['option']

    fieldsets = (
        (
            "Stammdaten",
            {
                "fields": (
                    "customer_number",
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Profil",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "phone_number",
                    "street",
                    "zip_code",
                    "city",
                    "country",
                    "zoom_link",
                )
            },
        ),
        (
            "Notizen",
            {
                "fields": (
                    "notes",
                )
            },
        ),
        (
            "Fortschritt",
            {
                "fields": (
                    "option",
                )
            },
        ),
        (
            "PAARBOX",
            {
                "fields": (
                    "paarbox_date",
                    "paarbox_present",
                    "paarbox_sent",
                    "paarbox_handed_over",
                )
            },
        ),

    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["url", "title"]
    actions = None
