# Generated by Django 4.2 on 2023-04-28 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0018_truckequipment_receivment'),
    ]

    operations = [
        migrations.AddField(
            model_name='semitrailerequipment',
            name='receivment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='API.vehiclereceivment'),
        ),
    ]