# Generated by Django 4.0.6 on 2022-07-08 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_alter_media_next'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='module',
            options={'base_manager_name': 'data', 'default_manager_name': 'data', 'get_latest_by': 'created', 'ordering': ['ordering', 'name'], 'verbose_name': 'Kapitel', 'verbose_name_plural': 'Kapitel'},
        ),
        migrations.AddField(
            model_name='module',
            name='ordering',
            field=models.IntegerField(default=0, verbose_name='Sortierung'),
        ),
    ]
