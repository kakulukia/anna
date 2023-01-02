# Generated by Django 4.1.4 on 2023-01-02 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0015_appointment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="appointment",
            options={
                "base_manager_name": "data",
                "default_manager_name": "data",
                "get_latest_by": "created",
                "ordering": ["date", "start_time"],
                "verbose_name": "Termin",
                "verbose_name_plural": "Termine",
            },
        ),
        migrations.AlterModelOptions(
            name="training",
            options={
                "base_manager_name": "data",
                "default_manager_name": "data",
                "get_latest_by": "created",
                "ordering": ["ordering"],
                "verbose_name": "Kurs",
                "verbose_name_plural": "Kurse",
            },
        ),
        migrations.AddField(
            model_name="training",
            name="ordering",
            field=models.IntegerField(default=0, verbose_name="Sortierung"),
        ),
    ]
