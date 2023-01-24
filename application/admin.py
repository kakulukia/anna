from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from .models import *


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


class MediaInline(admin.StackedInline):
    model = Media
    extra = 1


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['name', 'ordering']
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
                    "stick_to_the_plan",
                    "ordering"
                )
            },
        ),
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    actions = None
    list_display = ['name', 'ordering', 'next']
    list_filter = ['training']


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['name', 'ordering', 'length', 'next']
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
        "clone",
        "zoom",
        "option",
    )
    list_display_links = ['email', 'first_or_username']
    list_filter = ["is_superuser", ("zoom_link", admin.EmptyFieldListFilter)]
    actions = None
    ordering = ("-created",)
    readonly_fields = ["customer_link", 'option', "partner_link"]
    fieldsets = (
        (
            "Stammdaten",
            {
                "fields": (
                    "customer_link",
                    "first_name",
                    "last_name",
                    "email",
                    "partner_link",
                    "zoom_link",
                    "start_date",
                    "end_date",
                    "username",
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
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
    )

    def clone(self, user: User):
        if user.is_superuser:
            return ""
        url = reverse("clone-user", args=[user.id])
        button = f'<a href = "{url}" class="btn btn-outline-primary">klonen</a>'
        return mark_safe(button)
    clone.short_description = ""

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

    @admin.display(description='Lead')
    def customer_link(self, user: User):
        if user.customer_url:
            link = f'<a href="{user.customer_url}" target="_blank">In Close anzeigen</a>'
            return mark_safe(link)
        else:
            return '-'

    @admin.display(description='Partner')
    def partner_link(self, user: User):
        if user.contact_id and user.lead_id:
            partner = User.data.filter(lead_id=user.lead_id).exclude(id=user.id)
            if partner:
                partner = partner.get()
                link = f'<a href="{reverse("admin:users_user_change", args=[partner.id])}" >{partner.full_name}</a>'
            return mark_safe(link)
        else:
            return 'unbekannt'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["url", "title"]
    actions = None


@login_required
def clone_user(request, user_id):
    user = get_object_or_404(User.data.all(), id=user_id)
    user.id = None
    user.username += "1"
    user.save()

    for access in Access.data.filter(user_id=user_id):
        access.user_id = user.id
        access.id = None
        access.save()

    messages.success(request, f"{user.get_full_name()} geklont!")

    return HttpResponseRedirect(reverse("admin:users_user_change", args=[user.id]))


@admin.register(Appointment)
class EventAdmin(admin.ModelAdmin):
    ...


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'free', 'list_courses']
    actions = None

    def list_courses(self, product: Product):

        course_names = product.courses.values_list('name', flat=True)
        return ', '.join(course_names)

    list_courses.short_description = 'Kurse'
