# Generated by Django 4.2 on 2023-05-04 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0023_faultreportphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='own_truck',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]