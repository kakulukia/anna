from django.db import migrations
from django.utils.timezone import now


def active_member_default(user):
    if user.start_date and user.end_date:
        return user.start_date <= now().date() <= user.end_date
    return False


def update_active_member_new(apps, schema_editor):
    User = apps.get_model("users", "User")
    for obj in User.data.all():
        obj.active_member_new = active_member_default(obj)
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0019_user_active_member_new"),
    ]

    operations = [
        migrations.RunPython(update_active_member_new),
    ]
