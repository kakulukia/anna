# Generated by Django 4.1.5 on 2023-01-24 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_remove_user_customer_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="forum_name",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]