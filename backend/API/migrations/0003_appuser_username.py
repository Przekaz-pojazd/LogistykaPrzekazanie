# Generated by Django 4.2 on 2023-04-15 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_alter_appuser_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='username',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]