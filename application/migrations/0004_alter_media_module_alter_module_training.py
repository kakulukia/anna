# Generated by Django 4.0.5 on 2022-06-16 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_remove_media_prev_remove_module_prev_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.module', verbose_name='Kapitel'),
        ),
        migrations.AlterField(
            model_name='module',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.training', verbose_name='Kurs'),
        ),
    ]
