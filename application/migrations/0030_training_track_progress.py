# Generated by Django 4.2.4 on 2023-10-19 19:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0029_alter_product_can_view_zoom_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="training",
            name="track_progress",
            field=models.BooleanField(default=False),
        ),
    ]
