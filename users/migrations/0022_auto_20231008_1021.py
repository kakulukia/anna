# Generated by Django 4.2.4 on 2023-10-08 10:21

from django.db import migrations
from django.utils.timezone import now


def is_active(user):
    if user.start_date and user.end_date:
        return user.start_date <= now().date() <= user.end_date
    return False


def update_active_member_new(apps, schema_editor):
    User = apps.get_model("users", "User")

    for user in User.data.all():
        show_links = is_active(user)
        ic(user, show_links)
        user.can_view_zoom_link = show_links
        user.can_view_appointments = show_links
        user.can_view_forum = show_links
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0021_alter_user_can_view_appointments_and_more"),
    ]

    operations = [
        migrations.RunPython(update_active_member_new),
    ]
