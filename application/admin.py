from pyexpat import model
from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1


class MediaInline(admin.StackedInline):
    model = Media
    extra = 1


class TrainingAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]


class ModuleAdmin(admin.ModelAdmin):
    inlines = [MediaInline]


class AccessAdmin(admin.ModelAdmin):
    list_display = ('training', 'user', 'created_at')

    # @display(ordering='training__name', description='Training')
    def training(self, obj):
        return obj.training.name

    def user(self, obj):
        return obj.user.first_name


# admin.site.register(UploadPrivate)
# admin.site.register(ZoomLink)
# admin.site.register(Session)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Media)
admin.site.register(Access, AccessAdmin)
admin.site.register(Completed)


class AccessInline(admin.StackedInline):
    model = Access
    extra = 1


class ZoomLinkInline(admin.StackedInline):
    model = ZoomLink
    extra = 1
    max_num = 1


class ContactInfoInline(admin.StackedInline):
    model = Contact_Info
    extra = 1
    max_num = 1


class ValidityInline(admin.StackedInline):
    model = Validity
    extra = 1
    max_num = 1


class UserAdmin(BaseUserAdmin):
    inlines = [ValidityInline, ContactInfoInline, ZoomLinkInline, AccessInline]
    list_display = ('email', 'first_name', 'last_name',
                    'is_superuser', 'date_joined', 'option')
    list_filter = ('is_staff', 'is_superuser')
    verbose_name = "Customer"
    actions = None
    # list_display_links = ('see_progress', )

    def option(self, obj):
        # or anything you prefer e.g. an edit button
        from django.utils.html import mark_safe
        from django.urls import reverse
        if obj.is_superuser or not obj.email:
            return None
        user_id = obj.id
        url = reverse('progress-training', args=[user_id])
        element = f'<a href = "{url}" target="_blank" class = "btn btn-outline-primary" > Progress </a>'
        return mark_safe(element)
    option.short_description = "Fortschritt"

    fieldsets = (
        ('Benutzer',
            {'fields': (
                'first_name',
                'last_name',
                'email',
                'username',
                'password',
                'is_active',
                'is_staff',
                'is_superuser',
            )}
         ),
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['url', 'title']
    actions = None

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.site_header = 'Anna'
admin.site.site_title = 'Training platform'
admin.site.index_title = 'Admin'
