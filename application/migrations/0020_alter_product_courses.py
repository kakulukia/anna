# Generated by Django 4.1.5 on 2023-01-22 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0019_product_free"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="courses",
            field=models.ManyToManyField(to="application.training", verbose_name="Kurse"),
        ),
    ]
