# Generated by Django 4.2.6 on 2023-11-16 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_rename_image_employees_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='contact',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='employees',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
