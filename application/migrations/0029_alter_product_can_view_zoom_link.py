# Generated by Django 4.2.4 on 2023-10-08 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0028_merge_20231008_1055"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="can_view_zoom_link",
            field=models.BooleanField(default=False, verbose_name="Zoom-Link wird angezeigt"),
        ),
    ]