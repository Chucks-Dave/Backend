# Generated by Django 5.1.4 on 2024-12-31 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_graduate_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduate',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]