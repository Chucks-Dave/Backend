# Generated by Django 5.1.4 on 2024-12-31 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_customuser_options_customuser_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduate',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='cv'),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]
