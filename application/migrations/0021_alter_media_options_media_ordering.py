# Generated by Django 4.1.5 on 2023-01-24 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0020_alter_product_courses"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="media",
            options={
                "base_manager_name": "data",
                "default_manager_name": "data",
                "get_latest_by": "created",
                "ordering": ["ordering", "name"],
                "verbose_name": "Lektion",
                "verbose_name_plural": "Lektionen",
            },
        ),
        migrations.AddField(
            model_name="media",
            name="ordering",
            field=models.IntegerField(default=0, verbose_name="Sortierung"),
        ),
    ]
