# Generated by Django 4.2 on 2023-05-03 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0021_vehiclereceivment_sender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclereceivment',
            name='story',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]