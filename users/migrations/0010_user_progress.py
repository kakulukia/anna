# Generated by Django 4.0.6 on 2022-07-08 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_paarbox_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='progress',
            field=models.FloatField(default=0),
        ),
    ]