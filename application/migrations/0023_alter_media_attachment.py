# Generated by Django 4.1.5 on 2023-01-24 20:05

import application.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0022_media_attachment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="media",
            name="attachment",
            field=models.FileField(
                blank=True,
                null=True,
                storage=application.models.AttachmentStorage,
                upload_to="",
                verbose_name="Anhang",
            ),
        ),
    ]
