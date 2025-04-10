# Generated by Django 5.2 on 2025-04-10 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialMedia', '0014_alter_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, default='upload/User/placeholder.jpg', null=True, upload_to='upload/User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='upload/post'),
        ),
    ]
