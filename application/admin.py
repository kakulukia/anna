from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, F, OuterRef, Subquery, Value
from django.db.models.functions import Concat
from django.http import QueryDict
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from application.models import (
    Access,
    Appointment,
    Device,
    Media,
    Module,
    Page,
    Product,
    Training,
)
from users.models import User


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


class MediaInline(admin.StackedInline):
    model = Media
    extra = 1


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ["name", "ordering"]
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
                    "hide_after_x_days",
                    "ordering",
                    "assign_after_days",
                    "track_progress",
                )
            },
        ),
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    actions = None
    list_display = ["name", "ordering", "next"]
    list_filter = ["training"]


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    actions = None
    list_display = [
        "created",
        "name",
        "ordering",
        "length",
        "next",
        "attachment",
        "view_count",
    ]
    list_filter = ["module"]
    search_fields = ["name"]
    readonly_fields = ["copy"]
    actions = ["copy_action"]

    @admin.display(description="Kopieren")
    def copy(self, media: Media):
        chapter_list = Module.data.all().order_by("name")
        template = render_to_string("inc/copy.pug", {"chapter_list": chapter_list, "media_id": media.id})
        return template

    @admin.display(description="Views")
    def view_count(self, media: Media):
        return media.view_count

    def save_model(self, request, obj, form, change):
        if "file" in form.changed_data:
            obj.length = ""
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(view_count=Count("completed"))
        return qs


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
    title = "Status"
    parameter_name = "membership"

    def lookups(self, request, model_admin):
        return (
            ("teaser", "1x1"),
            ("intense", "intensiv"),
        )

    def queryset(self, request, queryset):
        timezone.now()
        if self.value() == "teaser":
            return queryset.filter(bought_teaser=True, bought_membership=False)
        if self.value() == "intense":
            return queryset.filter(bought_membership=True)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [AccessInline, DeviceInline]
    list_display = (
        "email",
        "forum_name",
        "first_or_username",
        "last_name",
        "other_user_name_display",
        "start_date",
        "end_date",
        "zoom",
        "status",
        "option",
    )
    list_display_links = ["email", "first_or_username"]
    list_filter = ["is_superuser", ("zoom_link", admin.EmptyFieldListFilter), MembershipFilter]
    actions = None
    ordering = ("-created",)
    readonly_fields = [
        "customer_link",
        "option",
        "partner_link",
        # "active_member_display"
    ]
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
            "Mitgliedschaft",
            {
                "fields": (
                    "option",
                    "bought_teaser",
                    "bought_membership",
                    "can_view_zoom_link",
                    "can_view_appointments",
                    "can_view_forum",
                )
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        subquery = (
            User.objects.filter(lead_id=OuterRef("lead_id"))
            .exclude(id=OuterRef("pk"))
            .annotate(other_user_name=Concat(F("first_name"), Value(" "), F("last_name")))
        )
        qs = qs.annotate(other_user_name=Subquery(subquery.values("other_user_name")))
        return qs

    # @admin.display(description="Aktives Mitglied")
    # def active_member_display(self, user: User):
    #     return user.active_member

    @admin.display(description="Partner")
    def other_user_name_display(self, user: User):
        return user.other_user_name

    def first_or_username(self, user: User):
        return user.first_name if user.first_name else user.username

    first_or_username.short_description = "Vorname"
    first_or_username.admin_order_field = "first_name"

    @admin.display(description="Zoom", boolean=True)
    def zoom(self, user: User):
        return bool(user.zoom_link)

    @admin.display(description="Status")
    def status(self, user: User):
        if user.bought_membership:
            return "intensiv"
        if user.bought_teaser:
            return "1x1"
        return "-"

    def option(self, obj):
        # or anything you prefer e.g. an edit button
        from django.urls import reverse
        from django.utils.html import mark_safe

        if obj.is_superuser or not obj.email:
            return None
        user_id = obj.id
        url = reverse("progress-training", args=[user_id])
        element = (
            f'<a href = "{url}" target="_blank" title="Fortschritt anzeigen">' f'<i class="far fa-chart-bar"></i></a>'
        )
        return mark_safe(element)

    option.short_description = "Fortschritt"

    @admin.display(description="Lead")
    def customer_link(self, user: User):
        if user.customer_url:
            link = f'<a href="{user.customer_url}" target="_blank">In Close anzeigen</a>'
            return mark_safe(link)
        else:
            return "-"

    @admin.display(description="Partner")
    def partner_link(self, user: User):
        if user.contact_id and user.lead_id:
            partner = User.data.filter(lead_id=user.lead_id).exclude(id=user.id)
            if partner:
                partner = partner.get()
                link = f'<a href="{reverse("admin:users_user_change", args=[partner.id])}" >' f"{partner.full_name}</a>"
                return mark_safe(link)
        return "unbekannt"


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["url", "title"]
    actions = None


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "clone_button"]

    @admin.display(description="")
    def clone_button(self, appointment: Appointment):
        data = QueryDict("", mutable=True)
        data.update(
            {
                "name": appointment.name,
                "start_time": appointment.start_time,
                "description": appointment.description,
                "link": appointment.link,
            }
        )

        # Construct the add URL with initial data
        add_url = reverse("admin:application_appointment_add")
        add_url += f"?{data.urlencode()}"

        return format_html(f'<a class="button" href="{add_url}">Klonen</a>')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "free", "teaser", "membership", "list_courses"]
    actions = None

    def list_courses(self, product: Product):
        course_names = product.courses.values_list("name", flat=True)
        return ", ".join(course_names)

    list_courses.short_description = "Kurse"
