# Generated by Django 4.2 on 2023-04-15 14:17

import backend.API.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_appuser_city_appuser_is_admin_appuser_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='mobile_phone',
            field=models.CharField(default='000000000', max_length=9, validators=[backend.API.models.mobile_address_valid]),
        ),
    ]
