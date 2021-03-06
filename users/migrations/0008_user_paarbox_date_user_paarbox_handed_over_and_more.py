# Generated by Django 4.0.5 on 2022-06-16 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_address_user_city_user_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='paarbox_date',
            field=models.DateField(blank=True, null=True, verbose_name='Datum'),
        ),
        migrations.AddField(
            model_name='user',
            name='paarbox_handed_over',
            field=models.BooleanField(default=False, verbose_name='übergeben'),
        ),
        migrations.AddField(
            model_name='user',
            name='paarbox_present',
            field=models.BooleanField(default=False, verbose_name='vorhanden'),
        ),
        migrations.AddField(
            model_name='user',
            name='paarbox_sent',
            field=models.BooleanField(default=False, verbose_name='vorsendet'),
        ),
    ]
