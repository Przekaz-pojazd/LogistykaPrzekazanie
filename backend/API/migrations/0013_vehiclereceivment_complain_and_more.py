# Generated by Django 4.2 on 2023-04-20 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0012_alter_vehiclereceivment_data_ended'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclereceivment',
            name='complain',
            field=models.CharField(choices=[('T', 'Tak'), ('N', 'Nie')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='vehiclereceivment',
            name='truck',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='API.truck'),
        ),
    ]