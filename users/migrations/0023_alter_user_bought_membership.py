# Generated by Django 4.2.4 on 2023-10-19 19:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0022_auto_20231008_1021"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="bought_membership",
            field=models.BooleanField(default=False, verbose_name="Intensivzeit"),
        ),
    ]
