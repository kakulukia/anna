# Generated by Django 4.1.5 on 2023-01-25 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0015_user_forum_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="forum_name",
            field=models.CharField(
                blank=True, max_length=40, null=True, verbose_name="Nutzername Forum"
            ),
        ),
    ]
