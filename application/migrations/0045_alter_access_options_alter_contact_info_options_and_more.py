# Generated by Django 4.0.3 on 2022-05-21 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0044_rename_phone_and_address_contact_info'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='access',
            options={'verbose_name': 'Media access', 'verbose_name_plural': 'Media access'},
        ),
        migrations.AlterModelOptions(
            name='contact_info',
            options={'verbose_name': 'Contact Info', 'verbose_name_plural': 'Contact Info'},
        ),
        migrations.AlterModelOptions(
            name='zoomlink',
            options={'verbose_name': 'Zoom Link', 'verbose_name_plural': 'Zoom Link'},
        ),
        migrations.CreateModel(
            name='Validity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Validity',
                'verbose_name_plural': 'Validity',
            },
        ),
    ]
