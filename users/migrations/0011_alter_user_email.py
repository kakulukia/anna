# Generated by Django 4.0.6 on 2022-07-19 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='E-Mail-Adresse'),
        ),
    ]
