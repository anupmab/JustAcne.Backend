# Generated by Django 3.2.7 on 2021-10-19 16:43

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_userimage_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.get_image_upload_path),
        ),
    ]