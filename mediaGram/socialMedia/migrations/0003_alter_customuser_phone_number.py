# Generated by Django 5.2 on 2025-04-08 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialMedia', '0002_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
