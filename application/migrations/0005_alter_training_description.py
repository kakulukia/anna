# Generated by Django 4.0.5 on 2022-06-16 20:09

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_alter_media_module_alter_module_training'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='description',
            field=django_quill.fields.QuillField(blank=True, null=True, verbose_name='Beschreibung'),
        ),
    ]