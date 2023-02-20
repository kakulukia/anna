from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery, F, Value
from django.db.models.functions import Concat
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
    list_display = ['name', 'ordering', 'length', 'next', 'attachment']
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


class MembershipFilter(admin.SimpleListFilter):
    title = 'Aktiv/Passiv'
    parameter_name = 'membership'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Aktiv'),
            ('inactive', 'Passiv'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'active':
            return queryset.filter(start_date__lte=now, end_date__gte=now)
        if self.value() == 'inactive':
            return queryset.exclude(start_date__lte=now, end_date__gte=now)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [AccessInline, DeviceInline]
    list_display = (
        "email",
        'forum_name',
        "first_or_username",
        "last_name",
        "other_user_name_display",
        "start_date",
        "end_date",
        "zoom",
        "status",
        "option",
    )
    list_display_links = ['email', 'first_or_username']
    list_filter = ["is_superuser", ("zoom_link", admin.EmptyFieldListFilter), MembershipFilter]
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
                    "forum_name",
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
                    "bought_teaser",
                    "bought_membership",
                )
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        subquery = User.objects.filter(lead_id=OuterRef('lead_id')).exclude(id=OuterRef('pk')).annotate(
            other_user_name=Concat(F('first_name'), Value(" "), F('last_name')))
        qs = qs.annotate(other_user_name=Subquery(subquery.values('other_user_name')))
        return qs

    @admin.display(description="Partner")
    def other_user_name_display(self, user: User):
        return user.other_user_name

    def first_or_username(self, user: User):
        return user.first_name if user.first_name else user.username
    first_or_username.short_description = "Vorname"
    first_or_username.admin_order_field = 'first_name'

    @admin.display(description='Zoom', boolean=True)
    def zoom(self, user: User):
        return bool(user.zoom_link)

    @admin.display(description='Status')
    def status(self, user: User):
        if user.bought_membership and user.active_member:
            return 'Aktiv'
        if user.bought_membership:
            return 'Passiv'
        if user.bought_teaser:
            return '1x1'
        return '-'

    def option(self, obj):
        # or anything you prefer e.g. an edit button
        from django.urls import reverse
        from django.utils.html import mark_safe

        if obj.is_superuser or not obj.email:
            return None
        user_id = obj.id
        url = reverse("progress-training", args=[user_id])
        element = f'<a href = "{url}" target="_blank" title="Fortschritt anzeigen"><i class="far fa-chart-bar"></i></a>'
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
        return 'unbekannt'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["url", "title"]
    actions = None


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
