# Generated by Django 5.1.4 on 2024-12-31 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_graduate_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='graduate',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
