# Generated by Django 4.2.4 on 2023-08-20 16:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0020_new_actve_member_field"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="active_member_new",
            new_name="active_member",
        ),
    ]