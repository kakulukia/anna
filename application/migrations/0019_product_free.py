# Generated by Django 4.1.5 on 2023-01-22 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0018_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="free",
            field=models.BooleanField(default=False, verbose_name="unbeschränkt"),
        ),
    ]