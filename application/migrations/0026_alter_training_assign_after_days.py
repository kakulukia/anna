# Generated by Django 4.2 on 2023-05-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0025_training_assign_after_days"),
    ]

    operations = [
        migrations.AlterField(
            model_name="training",
            name="assign_after_days",
            field=models.IntegerField(
                default=0,
                help_text="Wird nach der eingestellten Anzahl an Tagen in der Mitgliedschaft automatisch freigegeben.",
                verbose_name="Automatisch freigeben",
            ),
        ),
    ]
