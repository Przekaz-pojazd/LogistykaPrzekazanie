# Generated by Django 4.2 on 2023-04-23 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0015_semitrailer_avaiable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semitrailercomplainphoto',
            name='semitrailer_photo',
            field=models.ImageField(upload_to='media'),
        ),
        migrations.AlterField(
            model_name='truckcomplainphoto',
            name='truck_photo',
            field=models.ImageField(upload_to='media'),
        ),
    ]